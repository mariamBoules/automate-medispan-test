import os
import re
import shutil
import subprocess
from datetime import datetime

from db_config import (
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
    connect,
)
from run_pipeline import mapping as PIPELINE_TABLES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POST_LOAD_PATH = os.path.join(BASE_DIR, "schema", "post_load.sql")

# Tables populated from delimit files — must have rows after a successful deploy.
DATA_TABLES = sorted(set(PIPELINE_TABLES.values()))

# Rebuilt by post_load.sql rather than included in the mysqldump.
POST_LOAD_TABLES = ("medispan_ndc_mapping",)


def find_mysql_client():
    mysql = shutil.which("mysql")
    if mysql:
        return mysql

    program_files = os.environ.get("ProgramFiles", r"C:\Program Files")
    for subpath in (
        r"MySQL\MySQL Server 8.0\bin\mysql.exe",
        r"MySQL\MySQL Server 8.4\bin\mysql.exe",
    ):
        candidate = os.path.join(program_files, subpath)
        if os.path.isfile(candidate):
            return candidate

    raise FileNotFoundError(
        "mysql client not found on PATH. Install MySQL client tools or add mysql to PATH."
    )


def parse_tables_from_dump(dump_path):
    with open(dump_path, encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"CREATE TABLE `([^`]+)`", content)


def table_exists(cursor, database, table):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name = %s
        """,
        (database, table),
    )
    return cursor.fetchone()[0] > 0


def ensure_database(cursor, database):
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{database}` "
        "CHARACTER SET latin1 COLLATE latin1_swedish_ci"
    )


ARCHIVED_TABLE_RE = re.compile(r"^(?P<base>.+)_archived_\d{8}_\d{6}$")


def list_stale_archived_tables(cursor, database):
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name LIKE %s
        """,
        (database, "%\\_archived\\_%"),
    )
    return [row[0] for row in cursor.fetchall() if ARCHIVED_TABLE_RE.match(row[0])]


def cleanup_stale_archived_tables(cursor, database):
    """
    Remove or restore *_archived_* tables left by interrupted or failed deploys.

    If the live table already exists, the stale archive is dropped. If only the
    archive remains (deploy stopped after rename, before import), restore it.
    """
    cleaned = 0
    cursor.execute(f"USE `{database}`")

    for archived_name in list_stale_archived_tables(cursor, database):
        original = ARCHIVED_TABLE_RE.match(archived_name).group("base")
        if table_exists(cursor, database, original):
            cursor.execute(f"DROP TABLE `{archived_name}`")
        else:
            cursor.execute(f"RENAME TABLE `{archived_name}` TO `{original}`")
        cleaned += 1

    return cleaned


def archive_tables(cursor, database, tables, suffix):
    archived = {}
    cursor.execute(f"USE `{database}`")

    for table in tables:
        if not table_exists(cursor, database, table):
            continue

        archived_name = f"{table}_archived_{suffix}"
        if table_exists(cursor, database, archived_name):
            cursor.execute(f"DROP TABLE `{archived_name}`")

        cursor.execute(f"RENAME TABLE `{table}` TO `{archived_name}`")
        archived[table] = archived_name

    return archived


def rollback_archive(cursor, database, archived):
    if not archived:
        return

    cursor.execute(f"USE `{database}`")
    for original, archived_name in archived.items():
        if not table_exists(cursor, database, archived_name):
            continue
        if table_exists(cursor, database, original):
            cursor.execute(f"DROP TABLE `{original}`")
        cursor.execute(f"RENAME TABLE `{archived_name}` TO `{original}`")


def drop_archived_tables(cursor, archived):
    for archived_name in archived.values():
        cursor.execute(f"DROP TABLE IF EXISTS `{archived_name}`")


def import_dump(dump_path, database):
    mysql = find_mysql_client()
    with open(dump_path, "rb") as dump_file:
        result = subprocess.run(
            [
                mysql,
                "-h",
                MYSQL_HOST,
                "-P",
                str(MYSQL_PORT),
                "-u",
                MYSQL_USER,
                f"-p{MYSQL_PASSWORD}",
                database,
            ],
            stdin=dump_file,
            capture_output=True,
            text=True,
        )

    if result.returncode != 0:
        raise RuntimeError(f"mysql import failed:\n{result.stderr.strip()}")


def run_post_load(cursor):
    with open(POST_LOAD_PATH, encoding="utf-8") as f:
        sql = f.read()

    for stmt in sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)


def fix_view_definers(cursor, database):
    """
    Views copied from production often reference a DEFINER user that does not
    exist locally (e.g. rxmax_prod_user). That leaves data queryable but breaks
    many GUI clients when they fetch view metadata.
    """
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.views
        WHERE table_schema = %s
        """,
        (database,),
    )
    view_names = [row[0] for row in cursor.fetchall()]
    if not view_names:
        return 0

    fixed = 0
    for view_name in view_names:
        cursor.execute(f"SHOW CREATE VIEW `{database}`.`{view_name}`")
        create_sql = cursor.fetchone()[1]

        if "DEFINER=CURRENT_USER" in create_sql:
            continue
        if f"DEFINER=`{MYSQL_USER}`" in create_sql:
            continue

        create_sql = re.sub(
            r"DEFINER=`[^`]+`@`[^`]+`",
            "DEFINER=CURRENT_USER",
            create_sql,
            count=1,
        )
        create_sql = create_sql.replace("CREATE ", "CREATE OR REPLACE ", 1)
        cursor.execute(create_sql)
        fixed += 1

    return fixed


def verify_deployment(cursor, database, dump_tables, archived):
    cursor.execute(f"USE `{database}`")
    errors = []

    for table in DATA_TABLES:
        if table not in dump_tables:
            errors.append(f"Dump is missing expected data table: {table}")
            continue
        if not table_exists(cursor, database, table):
            errors.append(f"Missing table after import: {table}")
            continue

        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        if count == 0:
            errors.append(f"Table {table} has 0 rows")
            continue

        archived_name = archived.get(table)
        if archived_name and table_exists(cursor, database, archived_name):
            cursor.execute(f"SELECT COUNT(*) FROM `{archived_name}`")
            archived_count = cursor.fetchone()[0]
            if archived_count > 0 and count < archived_count * 0.5:
                errors.append(
                    f"Table {table} row count ({count}) is much lower than "
                    f"archived ({archived_count})"
                )

    for table in POST_LOAD_TABLES:
        if not table_exists(cursor, database, table):
            errors.append(f"Missing post-load table: {table}")
            continue

        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        if cursor.fetchone()[0] == 0:
            errors.append(f"Post-load table {table} has 0 rows")

    if errors:
        raise RuntimeError("Deployment verification failed:\n" + "\n".join(errors))


def verify_deployed_schema(database):
    """Lightweight post-deploy check (used by CI and manual verification)."""
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.schemata
            WHERE schema_name = %s
            """,
            (database,),
        )
        if cursor.fetchone()[0] == 0:
            raise RuntimeError(f"Schema `{database}` does not exist")

        cursor.execute(f"USE `{database}`")
        errors = []
        summary = []

        for table in DATA_TABLES:
            if not table_exists(cursor, database, table):
                errors.append(f"Missing table: {table}")
                continue

            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            count = cursor.fetchone()[0]
            summary.append(f"  {table}: {count:,} rows")
            if count == 0:
                errors.append(f"Table {table} has 0 rows")

        for table in POST_LOAD_TABLES:
            if not table_exists(cursor, database, table):
                errors.append(f"Missing post-load table: {table}")
                continue

            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            count = cursor.fetchone()[0]
            summary.append(f"  {table}: {count:,} rows")
            if count == 0:
                errors.append(f"Post-load table {table} has 0 rows")

        print(f"Deploy verification for `{database}`:")
        print("\n".join(summary))

        if errors:
            raise RuntimeError("Schema verification failed:\n" + "\n".join(errors))

        print("Deploy verification passed")
    finally:
        cursor.close()
        conn.close()


def deploy(dump_path, target_database):
    if not os.path.isfile(dump_path):
        raise FileNotFoundError(f"SQL dump not found: {dump_path}")

    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_tables = parse_tables_from_dump(dump_path)
    tables_to_archive = list(dict.fromkeys([*dump_tables, *POST_LOAD_TABLES]))

    archived = {}
    conn = connect()
    cursor = conn.cursor()

    try:
        ensure_database(cursor, target_database)
        conn.commit()

        stale = cleanup_stale_archived_tables(cursor, target_database)
        if stale:
            conn.commit()
            print(f"Cleaned up {stale} stale archived table(s) in `{target_database}`")

        archived = archive_tables(cursor, target_database, tables_to_archive, suffix)
        conn.commit()
        print(f"Archived {len(archived)} table(s) in `{target_database}`")

        import_dump(dump_path, target_database)
        print(f"Imported dump into `{target_database}`")

        cursor.execute(f"USE `{target_database}`")
        run_post_load(cursor)
        conn.commit()
        print("Ran post-load SQL (medispan_ndc_mapping + indexes)")

        views_fixed = fix_view_definers(cursor, target_database)
        conn.commit()
        if views_fixed:
            print(f"Updated DEFINER on {views_fixed} view(s) for local metadata access")

        verify_deployment(cursor, target_database, dump_tables, archived)
        print("Deployment verification passed")

        drop_archived_tables(cursor, archived)
        conn.commit()
        print(f"Dropped {len(archived)} archived table(s)")

    except Exception:
        conn.rollback()
        try:
            rollback_archive(cursor, target_database, archived)
            conn.commit()
            print("Rolled back archived tables after failure")
        except Exception as rollback_error:
            print(f"Rollback failed: {rollback_error}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    import sys

    from deploy_config import mock_database_name, resolve_deploy_plan

    if len(sys.argv) > 1 and sys.argv[1] == "--fix-views":
        database = mock_database_name()
        conn = connect()
        cursor = conn.cursor()
        try:
            cursor.execute(f"USE `{database}`")
            fixed = fix_view_definers(cursor, database)
            conn.commit()
            print(f"Updated DEFINER on {fixed} view(s) in `{database}`")
        finally:
            cursor.close()
            conn.close()
    else:
        plan = resolve_deploy_plan()
        dump_path = sys.argv[1] if len(sys.argv) > 1 else "medispan_dump.sql"
        if not plan.enabled or not plan.database:
            print(plan.skip_reason or "Deploy is disabled (DEPLOY_TARGET=none)")
            raise SystemExit(1)
        deploy(dump_path, plan.database)
