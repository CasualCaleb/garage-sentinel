from PIL import Image
from pathlib import Path
from db import database
import secrets
from models import File
from PIL import Image, ImageOps
from io import BytesIO

storage_path = Path(__file__).resolve().parent.parent / "storage"

# Initialize storage
if not storage_path.is_dir():
    storage_path.mkdir()

async def add_image(filename: str, image: Image.Image) -> int:
    storage_name = str(secrets.token_hex(nbytes=16))
    file_path = storage_path / storage_name

    try:
        image.save(file_path, image.format)

        file_id = await database.add_file(
            filename=filename,
            storage_name=storage_name
        )

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    return file_id

async def get_files() -> list[File]:
    return await database.get_files()

def get_thumbnail(file_path: Path) -> BytesIO:
    buffer = BytesIO()

    with Image.open(file_path) as image:
        img = ImageOps.exif_transpose(image)
        img.thumbnail((300, 300))

        img.convert("RGB").save(buffer, format="JPEG", quality=80)

    buffer.seek(0)
    return buffer