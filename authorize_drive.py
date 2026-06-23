import json
import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

import env_loader  # noqa: F401

SCOPES = ["https://www.googleapis.com/auth/drive"]
BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "google-oauth-token.json"


def main():
    secrets_file = os.environ.get(
        "GOOGLE_OAUTH_CLIENT_SECRETS_FILE",
        str(BASE_DIR / "oauth-client.json"),
    )
    secrets_path = Path(secrets_file)
    if not secrets_path.exists():
        raise SystemExit(
            f"\nMissing {secrets_path.name}\n\n"
            "One-time setup:\n"
            "1. Google Cloud Console → APIs & Services → Credentials\n"
            "2. Create Credentials → OAuth client ID → Desktop app\n"
            "3. Download JSON → save as oauth-client.json in this folder\n"
            "4. Run this script again\n"
        )

    with secrets_path.open(encoding="utf-8") as handle:
        client_info = json.load(handle)["installed"]

    flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), SCOPES)
    creds = flow.run_local_server(port=0)

    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")

    print(f"\nSaved: {TOKEN_PATH.name}")
    print("Upload is now enabled. Run: python main.py\n")
    print("For GitHub Actions, add these secrets:\n")
    print(f"GOOGLE_OAUTH_CLIENT_ID={client_info['client_id']}")
    print(f"GOOGLE_OAUTH_CLIENT_SECRET={client_info['client_secret']}")
    print(f"GOOGLE_OAUTH_REFRESH_TOKEN={creds.refresh_token}")


if __name__ == "__main__":
    main()
