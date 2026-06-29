"""
Pull the SQL dump from a Google Drive year/month folder and deploy it to the local
mock schema (mock-rxmax by default).

  python sync_mock_from_drive.py          # current year/month
  python sync_mock_from_drive.py 2026 5
"""

import argparse
import os
import sys

import env_loader  # noqa: F401

from deploy_config import mock_database_name
from deploy_database import deploy
from drive_utils import download_latest_sql_from_drive, has_drive_credentials
from pipeline_period import SQL_DUMP_FILENAME, format_period, resolve_period

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DUMP_PATH = os.path.join(BASE_DIR, SQL_DUMP_FILENAME)


def main():
    parser = argparse.ArgumentParser(
        description="Download SQL from a Drive year/month folder and deploy to local mock schema.",
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        help="Drive year folder (default: current year)",
    )
    parser.add_argument(
        "month",
        nargs="?",
        type=int,
        help="Drive month 1-12 (default: current month)",
    )
    parser.add_argument(
        "--dump-path",
        default=DEFAULT_DUMP_PATH,
        help=f"Where to save the downloaded SQL (default: {DEFAULT_DUMP_PATH})",
    )
    args = parser.parse_args()
    try:
        year, month = resolve_period(args.year, args.month)
    except ValueError as exc:
        parser.error(str(exc))

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
        f"← Drive SQL folder {format_period(year, month)}"
    )

    download_latest_sql_from_drive(args.dump_path, year, month)
    deploy(args.dump_path, database)
    print(
        f"\nLocal mock schema `{database}` is now in sync with "
        f"Drive {format_period(year, month)} pipeline output."
    )


if __name__ == "__main__":
    main()
