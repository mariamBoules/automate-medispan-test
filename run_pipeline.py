import os
import pandas as pd
import mysql.connector
import sys

DELIMIT_PATH = sys.argv[1]

# 🔁 Mapping (your confirmed mapping)
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
    "MF2VAL": "mf2val_d"
}

def clean_row(row, table_columns, numeric_columns):
    cleaned = []

    # Step 1: trim values
    for value in row:
        if isinstance(value, str):
            value = value.strip()
        cleaned.append(value)

    # Step 2: convert string nulls
    cleaned = [
        None if (isinstance(v, str) and v.lower() in ["nan", "none", "null"]) else v
        for v in cleaned
    ]

    # Step 3: 🔥 enforce column count (THIS replaces trailing logic)
    if len(cleaned) < len(table_columns):
        cleaned.extend([None] * (len(table_columns) - len(cleaned)))

    elif len(cleaned) > len(table_columns):
        cleaned = cleaned[:len(table_columns)]

    # Step 4: numeric columns → NULL instead of ""
    for i, value in enumerate(cleaned):
        col_name = table_columns[i]

        if value == "" and col_name in numeric_columns:
            cleaned[i] = None

    return cleaned
# 🔌 Connect (NO database yet)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()

# 🔥 STEP 0 — Reset DB
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("DROP DATABASE IF EXISTS medispan_test;")
cursor.execute("CREATE DATABASE medispan_test CHARACTER SET latin1;")
cursor.execute("USE medispan_test;")

print("✅ Database ready!")

# 🔥 STEP 1 — Create schema
print("⚙️ Creating schema...")

with open("schema/medispan_schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

for stmt in schema_sql.split(";"):
    stmt = stmt.strip()
    if stmt:
        try:
            cursor.execute(stmt)
        except Exception as e:
            print("⚠️ Skipping statement:", e)

conn.commit()
print("✅ Schema ready!")

# 🔥 STEP 2 — Load all files
for file_name, table_name in mapping.items():

    file_path = os.path.join(DELIMIT_PATH, file_name)

    if not os.path.exists(file_path):
        print(f"⚠️ File missing: {file_name}")
        continue

    print(f"\n📥 Loading {file_name} → {table_name}")

    df = pd.read_csv(
        file_path,
        delimiter="|",
        header=None,
        encoding="latin1",
        keep_default_na=False
    )

    # 🔥 Get schema info for THIS table
    cursor.execute(f"DESCRIBE {table_name}")
    columns_info = cursor.fetchall()

    table_columns = [col[0] for col in columns_info]

    numeric_columns = {
        col[0]
        for col in columns_info
        if any(t in col[1].lower() for t in ["int", "decimal", "float", "double", "bigint"])
    }

    # 🔥 Clean data correctly
    data = [
        clean_row(row, table_columns, numeric_columns)
        for row in df.values.tolist()
    ]

    # 🔧 Build insert query
    placeholders = ", ".join(["%s"] * len(df.columns))
    insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

    batch_size = 1000

    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        cursor.executemany(insert_sql, batch)
        conn.commit()
        print(f"✔ {table_name}: {i} → {i + len(batch)}")

print("\n🎉 ALL FILES LOADED SUCCESSFULLY!")

cursor.close()
conn.close()