"""
Pull the latest medispan_dump.sql from Google Drive and deploy it to the local
mock schema (mock-rxmax by default).

Use this after a GitHub Actions run so remote pipeline output shows up in your
local MySQL Workbench without giving CI access to your laptop.

  python sync_mock_from_drive.py
  python sync_mock_from_drive.py --year 2026 --month 6
"""

import argparse
import os
import sys

import env_loader  # noqa: F401

from deploy_config import mock_database_name
from deploy_database import deploy
from drive_utils import download_latest_sql_from_drive, has_drive_credentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DUMP_PATH = os.path.join(BASE_DIR, "medispan_dump.sql")


def main():
    parser = argparse.ArgumentParser(
        description="Download latest SQL from Drive and deploy to local mock schema.",
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Drive year folder (default: PIPELINE_YEAR or current year)",
    )
    parser.add_argument(
        "--month",
        type=int,
        help="Drive month folder (default: PIPELINE_MONTH or current month)",
    )
    parser.add_argument(
        "--dump-path",
        default=DEFAULT_DUMP_PATH,
        help=f"Where to save the downloaded SQL (default: {DEFAULT_DUMP_PATH})",
    )
    args = parser.parse_args()

    if args.year is not None:
        os.environ["PIPELINE_YEAR"] = str(args.year)
    if args.month is not None:
        os.environ["PIPELINE_MONTH"] = str(args.month)

    if not has_drive_credentials():
        print(
            "Google Drive credentials not found. "
            "Set GDRIVE_SERVICE_ACCOUNT_JSON or place gdrive-credentials.json in the project root.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    database = mock_database_name()
    print(f"Sync target: local mock schema `{database}` (from Drive → local MySQL)")

    download_latest_sql_from_drive(args.dump_path)
    deploy(args.dump_path, database)
    print(f"\nLocal mock schema `{database}` is now in sync with the latest remote pipeline output.")


if __name__ == "__main__":
    main()
