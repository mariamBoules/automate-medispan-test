import os
import pandas as pd
import mysql.connector
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATH = sys.argv[1]


# CHANGE TYPE in Excel -> (table, column)
CHANGE_TYPE_TO_DB = {
    "NDC": ("mf2ndc_h", "NDC_UPC_HRI"),
    "DDID Code": ("mf2ndc_h", "Drug_Descriptor_Identifier"),
    "Multi-Source Code": ("mf2ndc_h", "Multi_Source_Code"),
    "Labeler Code": ("mf2ndc_h", "Medi_Span_Labeler_Identifier"),
    "GPPC Code": ("mf2ndc_h", "Generic_Product_Packaging_Code"),
    "TEE Code": ("mf2ndc_h", "TEE_Code"),
    "PRODUCT NAME": ("mf2name_f", "Drug_Name"),
    "Dosage Form": ("mf2name_f", "Dosage_Form"),
    "Strength": ("mf2name_f", "Strength"),
    "Strength UOM": ("mf2name_f", "Strength_Unit_of_Measure"),
    "RXOTC Code": ("mf2ndc_h", "RX_OTC_Indicator_Code"),
    "Labeler Name": ("mf2lab_i", "Manufacturers_Labeler_Name"),
    "Pkg Size": ("mf2gppc_j", "Package_Size"),
    "Pkg Size UOM": ("mf2gppc_j", "Package_Size_Unit_of_Measure"),
}


def normalize(value):
    if pd.isna(value) or value is None:
        return ""

    value = str(value).strip()

    # 🔥 treat NA as empty
    if value.upper() in ["NA", "N/A"]:
        return ""

    return value

def get_db_value(cursor, ndc, table_name, column_name):
    """
    Fetch the current DB value for one NDC and one target column.
    """
    if table_name == "mf2ndc_h":
        query = f"""
            SELECT {column_name} AS value
            FROM mf2ndc_h
            WHERE NDC_UPC_HRI = %s
            LIMIT 1
        """
        cursor.execute(query, (ndc,))
        row = cursor.fetchone()
        return row["value"] if row else None

    if table_name == "mf2name_f":
        query = f"""
            SELECT nm.{column_name} AS value
            FROM mf2ndc_h n
            JOIN mf2name_f nm
              ON n.Drug_Descriptor_Identifier = nm.Drug_Descriptor_Identifier
            WHERE n.NDC_UPC_HRI = %s
            LIMIT 1
        """
        cursor.execute(query, (ndc,))
        row = cursor.fetchone()
        return row["value"] if row else None

    if table_name == "mf2lab_i":
        query = f"""
            SELECT l.{column_name} AS value
            FROM mf2ndc_h n
            JOIN mf2lab_i l
              ON n.Medi_Span_Labeler_Identifier = l.Medi_Span_Labeler_Identifier
            WHERE n.NDC_UPC_HRI = %s
            LIMIT 1
        """
        cursor.execute(query, (ndc,))
        row = cursor.fetchone()
        return row["value"] if row else None

    if table_name == "mf2gppc_j":
        query = f"""
            SELECT g.{column_name} AS value
            FROM mf2ndc_h n
            JOIN mf2gppc_j g
              ON n.Generic_Product_Packaging_Code = g.Generic_Product_Packaging_Code
            WHERE n.NDC_UPC_HRI = %s
            LIMIT 1
        """
        cursor.execute(query, (ndc,))
        row = cursor.fetchone()
        return row["value"] if row else None

    raise ValueError(f"Unsupported table: {table_name}")


def main():
    conn = mysql.connector.connect(
        host="localhost",
        user="medispan",
        password="mariam@",
        database="medispan_test"
    )
    cursor = conn.cursor(dictionary=True)

    df = pd.read_excel(EXCEL_PATH, engine="xlrd")

    # Adjust these if the actual sheet uses slightly different names
    NDC_COL = "NDC"
    CHANGE_TYPE_COL = "CHANGE TYPE"
    NEW_VAL_COL = "NEW VAL"

    errors = []
    skipped = []

    for idx, row in df.iterrows():
        ndc = normalize(row.get(NDC_COL))
        change_type = normalize(row.get(CHANGE_TYPE_COL))
        expected_new_val = normalize(row.get(NEW_VAL_COL))

        if not ndc or not change_type:
            skipped.append((idx, "Missing NDC or CHANGE TYPE"))
            continue

        if change_type not in CHANGE_TYPE_TO_DB:
            skipped.append((idx, ndc, change_type, "CHANGE TYPE not mapped"))
            continue

        table_name, column_name = CHANGE_TYPE_TO_DB[change_type]

        actual_db_val = get_db_value(cursor, ndc, table_name, column_name)
        actual_db_val = normalize(actual_db_val)

        if actual_db_val != expected_new_val:
            errors.append({
                "row_index": idx,
                "ndc": ndc,
                "change_type": change_type,
                "db_field": f"{table_name}.{column_name}",
                "expected_new_val": expected_new_val,
                "actual_db_val": actual_db_val,
            })

    cursor.close()
    conn.close()

    if skipped:
        print(f"\nSkipped rows: {len(skipped)}")
        for item in skipped[:10]:
            print(item)

    if errors:
        print(f"\nALIDATION FAILED — {len(errors)} mismatches\n")

        # convert to DataFrame
        errors_df = pd.DataFrame(errors)

        # save file
        output_path = os.path.join(BASE_DIR, "validation_errors.csv")
        errors_df.to_csv(output_path, index=False)

        print(f"📄 Errors saved to: {output_path}")

        raise SystemExit(1)

    else:
        print("\n✅ VALIDATION PASSED")


if __name__ == "__main__":
    main()