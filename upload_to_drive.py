import sys
from pathlib import Path

from drive_utils import upload_sql_to_drive
from pipeline_period import SQL_DUMP_FILENAME, parse_period_args

BASE_DIR = Path(__file__).resolve().parent


def main():
    year, month = parse_period_args()
    file_path = Path(BASE_DIR / SQL_DUMP_FILENAME)

    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])

    if not file_path.exists():
        raise SystemExit(f"File not found: {file_path}")

    upload_sql_to_drive(str(file_path), year, month)


if __name__ == "__main__":
    main()
