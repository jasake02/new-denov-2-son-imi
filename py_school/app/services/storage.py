import mimetypes
import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.database import STATIC_DIR

try:
    from vercel.blob import BlobClient
except ImportError:
    BlobClient = None

try:
    from vercel.blob import delete as delete_blob
except ImportError:
    delete_blob = None

BLOB_URL_MARKER = ".blob.vercel-storage.com"


def _discover_blob_token() -> str | None:
    direct_value = os.getenv("BLOB_READ_WRITE_TOKEN")
    if direct_value:
        return direct_value

    for key, value in os.environ.items():
        if value and "BLOB_READ_WRITE_TOKEN" in key:
            return value
    return None


def is_blob_url(path: str | None) -> bool:
    return bool(path and path.startswith("https://") and BLOB_URL_MARKER in path)


def is_local_upload_path(path: str | None) -> bool:
    return bool(path and path.startswith("/static/uploads/"))


def storage_uses_blob() -> bool:
    return bool(_discover_blob_token() and BlobClient is not None)


def save_upload_file(upload_file: UploadFile, folder: str = "uploads") -> str:
    if not upload_file or not upload_file.filename:
        return ""

    safe_folder = folder.strip("/\\") or "uploads"
    extension = Path(upload_file.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{extension}"
    content_type = upload_file.content_type or mimetypes.guess_type(upload_file.filename)[0] or "application/octet-stream"

    if storage_uses_blob():
        token = _discover_blob_token()
        file_bytes = upload_file.file.read()
        upload_file.file.seek(0)

        client = BlobClient(token=token)
        blob = client.put(
            f"{safe_folder}/{filename}",
            file_bytes,
            access="public",
            content_type=content_type,
            add_random_suffix=False,
            multipart=len(file_bytes) > 5 * 1024 * 1024,
        )
        return blob.url

    target_dir = STATIC_DIR / safe_folder
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / filename

    with target_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return f"/static/{safe_folder}/{filename}"


def delete_media(path: str | None) -> None:
    if not path:
        return

    if is_blob_url(path):
        if delete_blob is not None:
            delete_blob(path, token=_discover_blob_token())
        return

    if not is_local_upload_path(path):
        return

    relative_path = path.replace("/static/", "", 1).strip("/\\")
    file_path = STATIC_DIR / relative_path
    if file_path.exists():
        file_path.unlink()
