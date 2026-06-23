import os
from pathlib import Path

from dotenv import load_dotenv

# On GitHub Actions, use workflow env only — never a committed .env file.
if not os.environ.get("GITHUB_ACTIONS"):
    load_dotenv(Path(__file__).resolve().parent / ".env")
