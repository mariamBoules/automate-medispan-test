"""Resolve and validate the pipeline year/month (CLI, env, or GitHub Actions)."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime


def validate_month(month: int) -> int:
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    return month


def format_period(year: int, month: int) -> str:
    return f"{year}/{month:02d}"


def current_period() -> tuple[int, int]:
    now = datetime.now()
    return now.year, now.month


def resolve_period(year: int | None, month: int | None) -> tuple[int, int]:
    default_year, default_month = current_period()
    return (
        year if year is not None else default_year,
        validate_month(month if month is not None else default_month),
    )


SQL_DUMP_FILENAME = "medispan_dump.sql"


def parse_period_args(argv: list[str] | None = None) -> tuple[int, int]:
    parser = argparse.ArgumentParser(
        description="Run the medispan pipeline for a specific year/month.",
    )
    parser.add_argument(
        "year",
        nargs="?",
        type=int,
        help="Year folder (default: current year)",
    )
    parser.add_argument(
        "month",
        nargs="?",
        type=int,
        help="Month 1-12 (default: current month)",
    )
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

    try:
        return resolve_period(args.year, args.month)
    except ValueError as exc:
        parser.error(str(exc))


def apply_period_env(year: int, month: int) -> None:
    os.environ["PIPELINE_YEAR"] = str(year)
    os.environ["PIPELINE_MONTH"] = str(month)
