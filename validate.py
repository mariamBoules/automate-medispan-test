import os
import sys

import pandas as pd

from db_config import PIPELINE_DATABASE, connect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHANGE_TYPE_TO_DB = {
    "NDC": ("mf2ndc_h", "NDC_UPC_HRI"),
    "DDID Code": ("mf2ndc_h", "Drug_Descriptor_Identifier"),
    "Multi-Source Code": ("mf2ndc_h", "Multi_Source_Code"),
    "SUM": ("mf2gppc_j", "Package_Size_Unit_of_Measure"),
    "Labeler Code": ("mf2ndc_h", "Medi_Span_Labeler_Identifier"),
    "GPPC Code": ("mf2ndc_h", "Generic_Product_Packaging_Code"),
    "TEE Code": ("mf2ndc_h", "TEE_Code"),
    "DESI Code": ("mf2ndc_h", "DESI_Code"),
    "Third Party Code": ("mf2ndc_h", "Third_Party_Restriction_Code"),
    "Brand Name Code": ("mf2ndc_h", "Name_Type_Code"),
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
    if value.upper() in ["NA", "N/A"]:
        return ""

    return value


def normalize_ndc(value):
    value = normalize(value)
    if not value:
        return ""
    if value.endswith(".0") and value[:-2].isdigit():
        return value[:-2]
    return value


def ndc_lookup_candidates(ndc):
    ndc = normalize_ndc(ndc)
    if not ndc:
        return []

    candidates = [ndc]
    if ndc.isdigit():
        candidates.append(ndc.zfill(11))
    return list(dict.fromkeys(candidates))


def get_db_value(cursor, ndc, table_name, column_name):
    if table_name == "mf2ndc_h":
        query = f"""
            SELECT {column_name} AS value
            FROM mf2ndc_h
            WHERE NDC_UPC_HRI = %s
            LIMIT 1
        """
        for candidate in ndc_lookup_candidates(ndc):
            cursor.execute(query, (candidate,))
            row = cursor.fetchone()
            if row:
                return row["value"]
        return None

    if table_name == "mf2name_f":
        query = f"""
            SELECT nm.{column_name} AS value
            FROM mf2ndc_h n
            JOIN mf2name_f nm
              ON n.Drug_Descriptor_Identifier = nm.Drug_Descriptor_Identifier
            WHERE n.NDC_UPC_HRI = %s
            LIMIT 1
        """
    elif table_name == "mf2lab_i":
        query = f"""
            SELECT l.{column_name} AS value
            FROM mf2ndc_h n
            JOIN mf2lab_i l
              ON n.Medi_Span_Labeler_Identifier = l.Medi_Span_Labeler_Identifier
            WHERE n.NDC_UPC_HRI = %s
            LIMIT 1
        """
    elif table_name == "mf2gppc_j":
        query = f"""
            SELECT g.{column_name} AS value
            FROM mf2ndc_h n
            JOIN mf2gppc_j g
              ON n.Generic_Product_Packaging_Code = g.Generic_Product_Packaging_Code
            WHERE n.NDC_UPC_HRI = %s
            LIMIT 1
        """
    else:
        raise ValueError(f"Unsupported table: {table_name}")

    for candidate in ndc_lookup_candidates(ndc):
        cursor.execute(query, (candidate,))
        row = cursor.fetchone()
        if row:
            return row["value"]
    return None


def main(excel_path):
    conn = connect(database=PIPELINE_DATABASE)
    cursor = conn.cursor(dictionary=True)

    df = pd.read_excel(excel_path, engine="xlrd")
    df.columns = [str(col).strip() for col in df.columns]

    errors = []
    skipped = []
    unmapped = []
    validated_count = 0
    found_in_db_count = 0

    for idx, row in df.iterrows():
        ndc = normalize_ndc(row.get("NDC"))
        change_type = normalize(row.get("CHANGE TYPE"))
        expected_new_val = normalize(row.get("NEW VAL"))

        if not ndc or not change_type:
            skipped.append((idx, "Missing NDC or CHANGE TYPE"))
            continue

        if change_type not in CHANGE_TYPE_TO_DB:
            unmapped.append((idx, ndc, change_type))
            continue

        table_name, column_name = CHANGE_TYPE_TO_DB[change_type]
        actual_db_val = get_db_value(cursor, ndc, table_name, column_name)
        validated_count += 1
        if actual_db_val is not None:
            found_in_db_count += 1

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
        print("Skipped rows (sample):")
        for item in skipped[:10]:
            print(item)

    if unmapped:
        unmapped_types = sorted({change_type for _, _, change_type in unmapped})
        print(f"Unmapped CHANGE TYPE rows: {len(unmapped)} ({', '.join(unmapped_types)})")
        for item in unmapped[:10]:
            print(item)

        print(
            "\nVALIDATION FAILED: one or more rows use a CHANGE TYPE that is not mapped. "
            "Add the mapping in validate.py or fix the Excel file."
        )
        raise SystemExit(1)

    if validated_count == 0:
        print(
            "\nVALIDATION FAILED: no rows could be checked "
            "(Excel empty or every row missing NDC/CHANGE TYPE)."
        )
        raise SystemExit(1)

    if found_in_db_count == 0:
        print(
            "\nVALIDATION FAILED: none of the Excel change rows could be found in the database."
        )
        raise SystemExit(1)

    if errors:
        errors_df = pd.DataFrame(errors)
        output_path = os.path.join(BASE_DIR, "validation_errors.csv")
        errors_df.to_csv(output_path, index=False)
        print(f"Errors saved to: {output_path}")
        raise SystemExit(1)

    print(
        f"\nVALIDATION PASSED ({validated_count} row(s) checked against `{PIPELINE_DATABASE}`)"
    )


if __name__ == "__main__":
    main(sys.argv[1])
