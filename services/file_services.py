from pathlib import Path
from db import database
import secrets
from models import File, CreateFile
from PIL import Image, ImageOps
from io import BytesIO

storage_path = Path(__file__).resolve().parent.parent / "storage"

# Initialize storage
if not storage_path.is_dir():
    storage_path.mkdir()

async def add_file(user_id: int, filename: str, file_type: str, data: bytes) -> File:
    storage_name = str(secrets.token_hex(nbytes=16))
    file_path = storage_path / storage_name

    # Chop off the ext from the filename (To look pretty)
    filename = filename.rsplit(".", 1)[0]

    try:
        bytes_written = file_path.write_bytes(data)

        if bytes_written != len(data):
            raise IOError("Incomplete file write")

        file = await database.add_file(CreateFile(
            user_id=user_id,
            filename=filename,
            filetype=file_type,
            storage_name=storage_name
            )
        )

        return file

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

async def get_files(user_id: int, file_types: list[str] | None = None) -> list[File]:
    # Default to photos if no argument
    if file_types is None:
        file_types = ["png", "jpg", "jpeg"]

    return await database.get_files_by_user_id(user_id, file_types)

def get_thumbnail(file_path: Path) -> BytesIO:
    buffer = BytesIO()

    with Image.open(file_path) as image:
        img = ImageOps.exif_transpose(image)
        img.thumbnail((800, 800))

        img.convert("RGB").save(buffer, format="JPEG", quality=80)

    buffer.seek(0)
    return buffer