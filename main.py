import os
import sys
import zipfile
import subprocess
import shutil

# 🔥 Use same Python interpreter
python_executable = sys.executable

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EXTRACT_DIR = os.path.join(BASE_DIR, "input_data")

# -----------------------------------
# STEP 0 — FIND INPUT FILES
# -----------------------------------
print("🔍 Searching for input files in assets/...")

zip_path = None
excel_path = None

for file in os.listdir(ASSETS_DIR):
    file_path = os.path.join(ASSETS_DIR, file)

    if file.lower().endswith(".zip"):
        zip_path = file_path

    elif file.lower().endswith(".xls"):
        excel_path = file_path

if not zip_path:
    raise Exception("❌ No ZIP file found in assets/")
if not excel_path:
    raise Exception("❌ No Excel (.xls) file found in assets/")

print("✅ ZIP found:", zip_path)
print("✅ Excel found:", excel_path)

# -----------------------------------
# STEP 1 — CLEAN input_data
# -----------------------------------
print("🧹 Cleaning input_data/...")

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
print("📦 Extracting ZIP...")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

print("✅ Extracted to:", EXTRACT_DIR)

# -----------------------------------
# STEP 3 — FIND DELIMIT FOLDER
# -----------------------------------
print("🔍 Searching for DELIMIT folder...")

delimit_path = None

for root, dirs, files in os.walk(EXTRACT_DIR):
    if os.path.basename(root).upper() == "DELIMIT":
        delimit_path = root
        break

if not delimit_path:
    raise Exception("❌ DELIMIT folder not found")

print("✅ DELIMIT found:", delimit_path)

# -----------------------------------
# STEP 4 — RUN PIPELINE
# -----------------------------------
print("🚀 Running pipeline...")

subprocess.run(
    [python_executable, "run_pipeline.py", delimit_path],
    check=True
)

# -----------------------------------
# STEP 5 — RUN VALIDATION
# -----------------------------------
print("🔍 Running validation...")

subprocess.run(
    [python_executable, "validate.py", excel_path],
    check=True
)

# -----------------------------------
# STEP 6 — DUMP DATABASE
# -----------------------------------
print("💾 Dumping database...")

dump_path = os.path.join(BASE_DIR, "medispan_dump.sql")

with open(dump_path, "w") as f:
    result = subprocess.run(
    [
        "mysqldump",
        "--no-tablespaces",
        "-h", "127.0.0.1",     # 🔥 CRITICAL FIX
        "-P", "3306",
        "-u", "root",
        "-proot",
        "medispan_test"
    ],
    )

if result.returncode != 0:
    print("❌ Dump failed:")
    print(result.stderr)
    raise Exception("mysqldump failed")

print("✅ Dump saved at:", dump_path)

print("\n🎉 ALL DONE SUCCESSFULLY")