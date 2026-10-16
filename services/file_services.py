from operator import imatmul
from pathlib import Path
from starlette.datastructures import UploadFile
from fastapi import HTTPException
from db import database
import secrets
from models import File
from PIL import Image, ImageOps
from io import BytesIO

storage_path = Path(__file__).resolve().parent.parent / "storage"

# Initialize storage
if not storage_path.is_dir():
    storage_path.mkdir()

async def add_file(filename: str, file_type: str, data: bytes) -> int:
    storage_name = str(secrets.token_hex(nbytes=16))
    file_path = storage_path / storage_name

    # Chop off the ext from the filename (To look pretty)
    filename = filename.rsplit(".", 1)[0]

    try:
        file_path.write_bytes(data)

        file_id = await database.add_file(
            filename=filename,
            filetype=file_type,
            storage_name=storage_name
        )

        return file_id

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

async def get_photos() -> list[File]:
    return await database.get_files(["png", "jpg", "jpeg"])

async def get_videos() -> list[File]:
    return await database.get_files(["mp4"])

def get_thumbnail(file_path: Path) -> BytesIO:
    buffer = BytesIO()

    with Image.open(file_path) as image:
        img = ImageOps.exif_transpose(image)
        img.thumbnail((800, 800))

        img.convert("RGB").save(buffer, format="JPEG", quality=80)

    buffer.seek(0)
    return buffer