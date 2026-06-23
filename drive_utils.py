import env_loader  # noqa: F401 — loads .env before reading variables

import io
import json
import os
from datetime import datetime
from pathlib import Path

from google.oauth2 import credentials as oauth_credentials
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive"]
BASE_DIR = Path(__file__).resolve().parent
FOLDER_MIME = "application/vnd.google-apps.folder"
OAUTH_TOKEN_PATH = BASE_DIR / "google-oauth-token.json"


def _resolve_creds_path(creds_path):
    path = Path(creds_path)
    if not path.is_absolute():
        path = BASE_DIR / path
    return path


def has_drive_credentials():
    if os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON"):
        return True

    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path and _resolve_creds_path(creds_path).exists():
        return True

    return (BASE_DIR / "gdrive-credentials.json").exists()


def has_oauth_credentials():
    if OAUTH_TOKEN_PATH.exists():
        return True
    return bool(
        os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN")
        and os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        and os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    )


def has_upload_credentials():
    return has_oauth_credentials()


def get_oauth_credentials():
    if OAUTH_TOKEN_PATH.exists():
        creds = oauth_credentials.Credentials.from_authorized_user_file(
            str(OAUTH_TOKEN_PATH), SCOPES
        )
        if creds.expired:
            creds.refresh(Request())
            OAUTH_TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        return creds

    creds = oauth_credentials.Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_OAUTH_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_OAUTH_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return creds


def get_upload_service():
    if not has_oauth_credentials():
        raise RuntimeError(
            "Upload requires a one-time Google sign-in. "
            "Put oauth-client.json in the project root, then run: python authorize_drive.py"
        )
    return build("drive", "v3", credentials=get_oauth_credentials())


def get_credentials():
    json_content = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON")
    if json_content:
        info = json.loads(json_content)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path:
        resolved = _resolve_creds_path(creds_path)
        if resolved.exists():
            return service_account.Credentials.from_service_account_file(str(resolved), scopes=SCOPES)

    local_path = BASE_DIR / "gdrive-credentials.json"
    if local_path.exists():
        return service_account.Credentials.from_service_account_file(str(local_path), scopes=SCOPES)

    raise RuntimeError(
        "Google Drive credentials not found. "
        "Set GDRIVE_SERVICE_ACCOUNT_JSON, GOOGLE_APPLICATION_CREDENTIALS, "
        "or place gdrive-credentials.json in the project root."
    )


def get_service():
    return build("drive", "v3", credentials=get_credentials())


def list_children(service, parent_id, mime_type=None):
    query = f"'{parent_id}' in parents and trashed = false"
    if mime_type:
        query += f" and mimeType = '{mime_type}'"

    items = []
    page_token = None
    while True:
        response = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        items.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return items


def find_child_folder(service, parent_id, name):
    for item in list_children(service, parent_id, FOLDER_MIME):
        if item["name"] == name:
            return item["id"]
    return None


def find_child_folder_flexible(service, parent_id, candidates):
    for name in candidates:
        folder_id = find_child_folder(service, parent_id, name)
        if folder_id:
            return folder_id
    return None


def create_folder(service, parent_id, name):
    metadata = {
        "name": name,
        "mimeType": FOLDER_MIME,
        "parents": [parent_id],
    }
    return (
        service.files()
        .create(body=metadata, fields="id", supportsAllDrives=True)
        .execute()["id"]
    )


def month_folder_candidates(month):
    dt = datetime(2000, month, 1)
    return [f"{month:02d}", str(month), dt.strftime("%B"), dt.strftime("%b")]


def get_pipeline_year_month():
    year_raw = os.environ.get("PIPELINE_YEAR", "").strip()
    month_raw = os.environ.get("PIPELINE_MONTH", "").strip()
    now = datetime.now()
    year = int(year_raw) if year_raw else now.year
    month = int(month_raw) if month_raw else now.month
    return year, month


def ensure_year_month_folder(service, root_id, year, month):
    year_id = find_child_folder(service, root_id, str(year))
    if not year_id:
        year_id = create_folder(service, root_id, str(year))
        print(f"Created year folder: {year}")

    month_id = find_child_folder_flexible(service, year_id, month_folder_candidates(month))
    if not month_id:
        month_id = create_folder(service, year_id, f"{month:02d}")
        print(f"Created month folder: {year}/{month:02d}")

    return month_id


def find_latest_file(service, folder_id, extensions):
    normalized = {ext.lower().lstrip(".") for ext in extensions}
    files = [
        item
        for item in list_children(service, folder_id)
        if item.get("mimeType") != FOLDER_MIME
        and Path(item["name"]).suffix.lower().lstrip(".") in normalized
    ]
    if not files:
        raise FileNotFoundError(
            f"No {', '.join(sorted(normalized))} file found in Drive folder {folder_id}"
        )

    files.sort(key=lambda item: item.get("modifiedTime", ""), reverse=True)
    return files[0]


def download_file(service, file_id, dest_path):
    request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with io.FileIO(dest_path, "wb") as handle:
        downloader = MediaIoBaseDownload(handle, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()


def upload_file(service, file_path, folder_id):
    file_path = Path(file_path)
    metadata = {"name": file_path.name, "parents": [folder_id]}
    media = MediaFileUpload(str(file_path), resumable=True)
    return (
        service.files()
        .create(
            body=metadata,
            media_body=media,
            fields="id, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )


def download_inputs_from_drive(assets_dir):
    zip_root = os.environ.get("GDRIVE_ZIP_ROOT_FOLDER_ID")
    xls_root = os.environ.get("GDRIVE_XLS_ROOT_FOLDER_ID")
    if not zip_root or not xls_root:
        raise RuntimeError(
            "GDRIVE_ZIP_ROOT_FOLDER_ID and GDRIVE_XLS_ROOT_FOLDER_ID must be set."
        )

    service = get_service()
    year, month = get_pipeline_year_month()
    print(f"Using Drive year/month: {year}/{month:02d}")

    zip_folder_id = ensure_year_month_folder(service, zip_root, year, month)
    xls_folder_id = ensure_year_month_folder(service, xls_root, year, month)

    zip_file = find_latest_file(service, zip_folder_id, ["zip"])
    xls_file = find_latest_file(service, xls_folder_id, ["xls", "xlsx"])

    assets_path = Path(assets_dir)
    assets_path.mkdir(parents=True, exist_ok=True)

    zip_dest = assets_path / zip_file["name"]
    xls_dest = assets_path / xls_file["name"]

    download_file(service, zip_file["id"], zip_dest)
    download_file(service, xls_file["id"], xls_dest)

    print(f"Downloaded ZIP: {zip_dest}")
    print(f"Downloaded XLS: {xls_dest}")
    return str(zip_dest), str(xls_dest)


def upload_sql_to_drive(file_path):
    sql_root = os.environ.get("GDRIVE_SQL_ROOT_FOLDER_ID")
    if not sql_root:
        raise RuntimeError("GDRIVE_SQL_ROOT_FOLDER_ID is not set.")

    service = get_upload_service()
    year, month = get_pipeline_year_month()
    folder_id = ensure_year_month_folder(service, sql_root, year, month)
    result = upload_file(service, file_path, folder_id)
    link = result.get("webViewLink") or f"https://drive.google.com/file/d/{result['id']}/view"
    print(f"Uploaded SQL to Drive ({year}/{month:02d}): {link}")
    return result
