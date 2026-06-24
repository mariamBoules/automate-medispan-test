import os

import pandas as pd

from db_config import PIPELINE_DATABASE, connect

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

REQUIRED_DELIMIT_FILES = tuple(mapping.keys())

# MF2DICT implied-decimal fields (flag Y + decimal places).
IMPLIED_DECIMALS = {
    ("mf2gppc_j", "Package_Size"): 3,
    ("mf2gpr_l", "Unit_Price"): 6,
    ("mf2prc_m", "Unit_Price"): 6,
    ("mf2prc_m", "Unit_Price___Extended"): 5,
    ("mf2prc_m", "Package_Price"): 2,
}

# Character-coded IDs that must keep leading zeros.
VARCHAR_PAD = {
    ("mf2ndc_h", "NDC_UPC_HRI"): 11,
    ("mf2ndc_h", "Old_NDC_UPC_HRI"): 11,
    ("mf2ndc_h", "New_NDC_UPC_HRI"): 11,
    ("mf2ndc_h", "Generic_Product_Packaging_Code"): 8,
    ("mf2ndcm_o", "NDC_UPC_HRI"): 11,
    ("mf2prc_m", "NDC_UPC_HRI"): 11,
    ("mf2gppc_j", "Generic_Product_Packaging_Code"): 8,
    ("mf2gpr_l", "Generic_Product_Packaging_Code"): 8,
}


def _is_null_token(value):
    return isinstance(value, str) and value.lower() in ("nan", "none", "null")


def _apply_implied_decimal(value, places):
    return int(value) / (10**places)


def _transform_value(table_name, col_name, value, numeric_columns):
    if _is_null_token(value):
        return None

    if isinstance(value, str):
        value = value.strip()

    if value == "":
        return None if col_name in numeric_columns else value

    pad_len = VARCHAR_PAD.get((table_name, col_name))
    if pad_len and isinstance(value, str) and value.isdigit():
        value = value.zfill(pad_len)

    decimal_places = IMPLIED_DECIMALS.get((table_name, col_name))
    if decimal_places is not None:
        return _apply_implied_decimal(value, decimal_places)

    if col_name in numeric_columns:
        if isinstance(value, str) and value.isdigit():
            return int(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return int(value) if float(value).is_integer() else value

    return value


def clean_row(row, table_name, table_columns, numeric_columns):
    cleaned = list(row)

    if len(cleaned) < len(table_columns):
        cleaned.extend([""] * (len(table_columns) - len(cleaned)))
    elif len(cleaned) > len(table_columns):
        cleaned = cleaned[: len(table_columns)]

    return [
        _transform_value(table_name, col_name, value, numeric_columns)
        for col_name, value in zip(table_columns, cleaned)
    ]


def validate_delimit_folder(delimit_path):
    missing = [
        file_name
        for file_name in REQUIRED_DELIMIT_FILES
        if not os.path.exists(os.path.join(delimit_path, file_name))
    ]
    if missing:
        raise FileNotFoundError(
            "DELIMIT folder is missing required medispan files: "
            + ", ".join(missing)
            + f"\nFolder checked: {delimit_path}"
            + "\nIf this came from Google Drive, ensure the month folder contains "
            "the single complete .zip (not split parts like ...-3-001.zip)."
        )


def run(delimit_path):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute(f"DROP DATABASE IF EXISTS `{PIPELINE_DATABASE}`;")
    cursor.execute(
        f"CREATE DATABASE `{PIPELINE_DATABASE}` CHARACTER SET latin1"
    )
    cursor.execute(f"USE `{PIPELINE_DATABASE}`;")

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

    validate_delimit_folder(delimit_path)

    for file_name, table_name in mapping.items():
        file_path = os.path.join(delimit_path, file_name)

        df = pd.read_csv(
            file_path,
            delimiter="|",
            header=None,
            encoding="latin1",
            dtype=str,
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

        data = [
            clean_row(row, table_name, table_columns, numeric_columns)
            for row in df.values.tolist()
        ]
        placeholders = ", ".join(["%s"] * len(table_columns))
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for i in range(0, len(data), 1000):
            batch = data[i : i + 1000]
            cursor.executemany(insert_sql, batch)
            conn.commit()

        print(f"Loaded {len(data):,} row(s) into {table_name}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    import sys

    run(sys.argv[1])
