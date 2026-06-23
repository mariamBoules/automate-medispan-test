import env_loader  # noqa: F401 — loads .env before reading variables

import os
import sys


def _require(name):
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value


MYSQL_HOST = _require("MYSQL_HOST")
MYSQL_PORT = int(_require("MYSQL_PORT"))
MYSQL_USER = _require("MYSQL_USER")
MYSQL_PASSWORD = _require("MYSQL_PASSWORD")
MYSQL_DATABASE = _require("MYSQL_DATABASE")


def connect(**kwargs):
    import mysql.connector

    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        **kwargs,
    )
