"""
Verify that deploy landed on MySQL. Intended for GitHub Actions after main.py.

Fails with a non-zero exit code if expected tables are missing or empty.
"""

import sys

import env_loader  # noqa: F401

from deploy_config import mock_database_name, resolve_deploy_plan
from deploy_database import verify_deployed_schema


def main():
    plan = resolve_deploy_plan()
    database = plan.database or mock_database_name()

    if not plan.enabled:
        print(
            "Deploy was skipped in this run — nothing to verify. "
            "Set DEPLOY_SKIP_ON_CI=false in the workflow to test deploy on CI.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    verify_deployed_schema(database)


if __name__ == "__main__":
    main()
