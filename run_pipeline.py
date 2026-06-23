import os

import pandas as pd

from db_config import connect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema", "medispan_schema.sql")

mapping = {
    "MF2GPPC": "mf2gppc_j",
    "MF2GPR": "mf2gpr_l",
    "MF2LAB": "mf2lab_i",
    "MF2MOD": "mf2mod_n",
    "MF2NAME": "mf2name_f",
    "MF2NDC": "mf2ndc_h",
    "MF2NDCM": "mf2ndcm_o",
    "MF2PRC": "mf2prc_m",
    "MF2SEC": "mf2sec_3",
    "MF2SUM": "mf2sum_a",
    "MF2TCGPI": "mf2tcgpi_g",
    "MF2VAL": "mf2val_d",
}


def clean_row(row, table_columns, numeric_columns):
    cleaned = []

    for value in row:
        if isinstance(value, str):
            value = value.strip()
        cleaned.append(value)

    cleaned = [
        None if (isinstance(v, str) and v.lower() in ["nan", "none", "null"]) else v
        for v in cleaned
    ]

    if len(cleaned) < len(table_columns):
        cleaned.extend([None] * (len(table_columns) - len(cleaned)))
    elif len(cleaned) > len(table_columns):
        cleaned = cleaned[: len(table_columns)]

    for i, value in enumerate(cleaned):
        col_name = table_columns[i]
        if value == "" and col_name in numeric_columns:
            cleaned[i] = None

    return cleaned


def run(delimit_path):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP DATABASE IF EXISTS medispan_test;")
    cursor.execute("CREATE DATABASE medispan_test CHARACTER SET latin1;")
    cursor.execute("USE medispan_test;")

    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(
            f"Missing schema file: {SCHEMA_PATH}\n"
            "Restore it with: git restore schema/medispan_schema.sql"
        )

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    for stmt in schema_sql.split(";"):
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except Exception:
                continue

    conn.commit()

    for file_name, table_name in mapping.items():
        file_path = os.path.join(delimit_path, file_name)

        if not os.path.exists(file_path):
            print(f"File missing: {file_name}")
            continue

        df = pd.read_csv(
            file_path,
            delimiter="|",
            header=None,
            encoding="latin1",
            keep_default_na=False,
        )

        cursor.execute(f"DESCRIBE {table_name}")
        columns_info = cursor.fetchall()
        table_columns = [col[0] for col in columns_info]
        numeric_columns = {
            col[0]
            for col in columns_info
            if any(t in col[1].lower() for t in ["int", "decimal", "float", "double", "bigint"])
        }

        data = [clean_row(row, table_columns, numeric_columns) for row in df.values.tolist()]
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for i in range(0, len(data), 1000):
            batch = data[i : i + 1000]
            cursor.executemany(insert_sql, batch)
            conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    import sys

    run(sys.argv[1])
