"""
Deploy target resolution.

Targets:
  mock        — deploy to DEPLOY_MOCK_DATABASE (default: mock-rxmax on MYSQL_HOST)
  production  — deploy to DEPLOY_PRODUCTION_DATABASE on MYSQL_HOST when
                DEPLOY_ALLOW_PRODUCTION=true; otherwise MOCKED → mock database
  none        — skip deploy

On GitHub Actions, deploy runs against the runner's temporary MySQL by default
(CI smoke test). That proves the deploy step works on Linux/GitHub the same way
as locally. It does not update your laptop — use sync_mock_from_drive.py for that.

Set DEPLOY_SKIP_ON_CI=true to skip deploy on GitHub Actions entirely.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from db_config import MYSQL_HOST


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def mock_database_name() -> str:
    # DEPLOY_DATABASE is a legacy alias for DEPLOY_MOCK_DATABASE.
    return (
        os.environ.get("DEPLOY_MOCK_DATABASE")
        or os.environ.get("DEPLOY_DATABASE")
        or "mock-rxmax"
    ).strip()


def production_database_name() -> str:
    return os.environ.get("DEPLOY_PRODUCTION_DATABASE", "").strip()


@dataclass(frozen=True)
class DeployPlan:
    enabled: bool
    database: str | None
    target: str
    is_mock_redirect: bool
    skip_reason: str | None = None

    @property
    def label(self) -> str:
        if not self.enabled:
            return "skipped"
        if self.is_mock_redirect:
            return f"production (mocked → `{self.database}`)"
        return f"{self.target} (`{self.database}`)"


def resolve_deploy_plan() -> DeployPlan:
    target = os.environ.get("DEPLOY_TARGET", "mock").strip().lower()
    mock_db = mock_database_name()
    prod_db = production_database_name()
    allow_production = _env_bool("DEPLOY_ALLOW_PRODUCTION")
    skip_on_ci = _env_bool("DEPLOY_SKIP_ON_CI")

    if target == "none":
        return DeployPlan(False, None, "none", False, "DEPLOY_TARGET=none")

    if skip_on_ci and os.environ.get("GITHUB_ACTIONS"):
        return DeployPlan(
            False,
            None,
            target,
            False,
            "Deploy skipped on CI (runner MySQL is temporary). "
            "After the workflow finishes, run on your PC: python sync_mock_from_drive.py YEAR MONTH",
        )

    if target == "mock":
        return DeployPlan(True, mock_db, "mock", False)

    if target == "production":
        if allow_production:
            if not prod_db:
                raise ValueError(
                    "DEPLOY_PRODUCTION_DATABASE must be set when DEPLOY_ALLOW_PRODUCTION=true"
                )
            return DeployPlan(True, prod_db, "production", False)

        return DeployPlan(
            True,
            mock_db,
            "production",
            True,
        )

    raise ValueError(f"Unknown DEPLOY_TARGET={target!r} (use mock, production, or none)")


def describe_deploy_plan(plan: DeployPlan) -> str:
    if not plan.enabled:
        lines = [f"Deploy: skipped ({plan.skip_reason or plan.target})"]
    elif plan.is_mock_redirect:
        lines = [
            "Deploy: production target is MOCKED (DEPLOY_ALLOW_PRODUCTION is not enabled)",
            f"  → will apply dump to `{plan.database}` on {MYSQL_HOST} instead of RDS",
            "  → set DEPLOY_ALLOW_PRODUCTION=true and DEPLOY_PRODUCTION_DATABASE when ready for real RDS",
        ]
    else:
        lines = [
            f"Deploy: {plan.target} → `{plan.database}` on {MYSQL_HOST}",
        ]

    if plan.enabled and os.environ.get("GITHUB_ACTIONS"):
        lines.append(
            "  (CI smoke test on the GitHub runner's temporary MySQL — "
            "sync_mock_from_drive.py updates your local Workbench copy)"
        )

    return "\n".join(lines)
