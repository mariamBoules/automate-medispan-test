import os
import sys
import zipfile
import subprocess
import shutil

import env_loader  # noqa: F401 — loads .env before reading variables

from db_config import (
    MYSQL_DATABASE,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
)
from deploy_config import describe_deploy_plan, resolve_deploy_plan
from deploy_database import deploy as deploy_database
from drive_utils import download_inputs_from_drive, has_drive_credentials, has_upload_credentials, upload_sql_to_drive
from run_pipeline import run as run_pipeline
from validate import main as run_validation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EXTRACT_DIR = os.path.join(BASE_DIR, "input_data")

# -----------------------------------
# STEP 0 — FIND INPUT FILES
# -----------------------------------

os.makedirs(ASSETS_DIR, exist_ok=True)

use_drive_inputs = (
    os.environ.get("GDRIVE_ZIP_ROOT_FOLDER_ID")
    and os.environ.get("GDRIVE_XLS_ROOT_FOLDER_ID")
    and has_drive_credentials()
)

if use_drive_inputs:
    for item in os.listdir(ASSETS_DIR):
        item_path = os.path.join(ASSETS_DIR, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

    zip_path, excel_path = download_inputs_from_drive(ASSETS_DIR)
else:
    if (
        os.environ.get("GDRIVE_ZIP_ROOT_FOLDER_ID")
        and os.environ.get("GDRIVE_XLS_ROOT_FOLDER_ID")
        and not has_drive_credentials()
    ):
        print("Using assets/ (Drive folders configured but credentials file not found)")

    zip_path = None
    excel_path = None

    for file in os.listdir(ASSETS_DIR):
        file_path = os.path.join(ASSETS_DIR, file)

        if file.lower().endswith(".zip"):
            zip_path = file_path
        elif file.lower().endswith(".xls"):
            excel_path = file_path

    if not zip_path:
        raise Exception("No ZIP file found in assets/")
    if not excel_path:
        raise Exception("No Excel (.xls) file found in assets/")

print("ZIP found:", zip_path)
print("Excel found:", excel_path)

# -----------------------------------
# STEP 1 — CLEAN input_data
# -----------------------------------

if os.path.exists(EXTRACT_DIR):
    for item in os.listdir(EXTRACT_DIR):
        item_path = os.path.join(EXTRACT_DIR, item)

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
else:
    os.makedirs(EXTRACT_DIR)

# -----------------------------------
# STEP 2 — UNZIP
# -----------------------------------

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

# -----------------------------------
# STEP 3 — FIND DELIMIT FOLDER
# -----------------------------------

delimit_path = None

for root, dirs, files in os.walk(EXTRACT_DIR):
    if os.path.basename(root).upper() == "DELIMIT":
        delimit_path = root
        break

if not delimit_path:
    raise Exception("DELIMIT folder not found")

# -----------------------------------
# STEP 4 — RUN PIPELINE
# -----------------------------------

run_pipeline(delimit_path)

# -----------------------------------
# STEP 5 — RUN VALIDATION
# -----------------------------------

run_validation(excel_path)

# -----------------------------------
# STEP 6 — DUMP DATABASE
# -----------------------------------

dump_path = os.path.join(BASE_DIR, "medispan_dump.sql")

with open(dump_path, "w") as f:
    result = subprocess.run(
        [
            "mysqldump",
            "--no-tablespaces",
            "-h", MYSQL_HOST,
            "-P", str(MYSQL_PORT),
            "-u", MYSQL_USER,
            f"-p{MYSQL_PASSWORD}",
            MYSQL_DATABASE,
        ],
        stdout=f,
        stderr=subprocess.PIPE,
        text=True
    )

if result.returncode != 0:
    print("Dump failed:")
    print(result.stderr)
    raise Exception("mysqldump failed")

print("Dump saved at:", dump_path)

# -----------------------------------
# STEP 7 — PUBLISH (Google Drive + target schema)
# -----------------------------------

publish_errors = []

if os.environ.get("GDRIVE_SQL_ROOT_FOLDER_ID") and has_upload_credentials():
    try:
        upload_sql_to_drive(dump_path)
    except Exception as exc:
        publish_errors.append(f"Google Drive upload failed: {exc}")
elif os.environ.get("GDRIVE_SQL_ROOT_FOLDER_ID"):
    print(
        "\nSQL dump saved locally, but Drive upload was skipped.\n"
        "One-time fix:\n"
        "  1. Save OAuth Desktop client JSON as oauth-client.json\n"
        "  2. Run: python authorize_drive.py\n"
        "  3. Run: python main.py again\n"
    )
else:
    print("Skipping Google Drive upload (GDRIVE_SQL_ROOT_FOLDER_ID not set)")

deploy_plan = resolve_deploy_plan()
print(describe_deploy_plan(deploy_plan))

if deploy_plan.enabled and deploy_plan.database:
    try:
        deploy_database(dump_path, deploy_plan.database)
        print(f"Deploy complete ({deploy_plan.label})")
    except Exception as exc:
        publish_errors.append(f"Database deploy failed: {exc}")
elif deploy_plan.skip_reason:
    print(deploy_plan.skip_reason)

if publish_errors:
    for message in publish_errors:
        print(message, file=sys.stderr)
    raise SystemExit(1)
