"""
Pull the SQL dump from a Google Drive year/month folder and deploy it to the local
mock schema (mock-rxmax by default).

  python sync_mock_from_drive.py 2026 5
"""

import argparse
import os
import sys

import env_loader  # noqa: F401

from deploy_config import mock_database_name
from deploy_database import deploy
from drive_utils import download_latest_sql_from_drive, has_drive_credentials
from pipeline_period import SQL_DUMP_FILENAME

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DUMP_PATH = os.path.join(BASE_DIR, SQL_DUMP_FILENAME)


def main():
    parser = argparse.ArgumentParser(
        description="Download SQL from a Drive year/month folder and deploy to local mock schema.",
    )
    parser.add_argument("year", type=int, help="Drive year folder (e.g. 2026)")
    parser.add_argument("month", type=int, help="Drive month 1-12 (e.g. 5 for May)")
    parser.add_argument(
        "--dump-path",
        default=DEFAULT_DUMP_PATH,
        help=f"Where to save the downloaded SQL (default: {DEFAULT_DUMP_PATH})",
    )
    args = parser.parse_args()

    if not 1 <= args.month <= 12:
        parser.error("month must be between 1 and 12")

    if not has_drive_credentials():
        print(
            "Google Drive credentials not found. "
            "Set GDRIVE_SERVICE_ACCOUNT_JSON or place gdrive-credentials.json in the project root.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    database = mock_database_name()
    print(
        f"Sync target: `{database}` on local MySQL "
        f"← Drive SQL folder {args.year}/{args.month:02d}"
    )

    download_latest_sql_from_drive(args.dump_path, args.year, args.month)
    deploy(args.dump_path, database)
    print(
        f"\nLocal mock schema `{database}` is now in sync with "
        f"Drive {args.year}/{args.month:02d} pipeline output."
    )


if __name__ == "__main__":
    main()
