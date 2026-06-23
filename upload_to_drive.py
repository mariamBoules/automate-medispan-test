import sys
from pathlib import Path

from drive_utils import upload_sql_to_drive

BASE_DIR = Path(__file__).resolve().parent


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else str(BASE_DIR / "medispan_dump.sql")

    if not Path(file_path).exists():
        raise SystemExit(f"File not found: {file_path}")

    upload_sql_to_drive(file_path)


if __name__ == "__main__":
    main()
