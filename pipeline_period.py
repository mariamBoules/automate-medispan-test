"""Resolve and validate the pipeline year/month (CLI, env, or GitHub Actions)."""

from __future__ import annotations

import argparse
import os
import sys


def validate_month(month: int) -> int:
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    return month


def format_period(year: int, month: int) -> str:
    return f"{year}/{month:02d}"


SQL_DUMP_FILENAME = "medispan_dump.sql"


def parse_period_args(argv: list[str] | None = None) -> tuple[int, int]:
    parser = argparse.ArgumentParser(
        description="Run the medispan pipeline for a specific year/month.",
    )
    parser.add_argument("year", nargs="?", type=int, help="Year folder (e.g. 2026)")
    parser.add_argument("month", nargs="?", type=int, help="Month 1-12 (e.g. 4 for April)")
    args = parser.parse_args(argv)

    if os.environ.get("GITHUB_ACTIONS"):
        year_raw = os.environ.get("PIPELINE_YEAR", "").strip()
        month_raw = os.environ.get("PIPELINE_MONTH", "").strip()
        if not year_raw or not month_raw:
            print(
                "GitHub Actions requires year and month workflow inputs "
                "(e.g. year=2026, month=4).",
                file=sys.stderr,
            )
            raise SystemExit(1)
        return int(year_raw), validate_month(int(month_raw))

    if args.year is None or args.month is None:
        parser.error("year and month are required (e.g. python main.py 2026 4)")

    return args.year, validate_month(args.month)


def apply_period_env(year: int, month: int) -> None:
    os.environ["PIPELINE_YEAR"] = str(year)
    os.environ["PIPELINE_MONTH"] = str(month)
