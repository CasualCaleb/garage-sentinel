import re
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from services import file_services
from services.file_services import storage_path, get_thumbnail

router = APIRouter()

accepted_file_types = ["PNG", "JPG", "JPEG"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def validate_image(file: UploadFile) -> Image.Image:
    contents = await file.read(MAX_FILE_SIZE + 1)

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds 10MB limit")

    try:
        image = Image.open(BytesIO(contents))

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status_code=415, detail="File type not supported")

    if not image.format in accepted_file_types:
        raise HTTPException(status_code=415, detail="File type not supported")

    return image

@router.post("/file")
async def upload_image(file: UploadFile = File(...)):
    filename = file.filename
    image = await validate_image(file)

    if not isinstance(filename, str):
        raise HTTPException(status_code=400, detail="Filename missing")

    file_id = await file_services.add_image(filename, image)

    return isinstance(file_id, int)

@router.get("/file/{storage_name}")
async def get_file(storage_name: str, size: str = "original"):
    if not re.fullmatch(r"[0-9a-f]{32}", storage_name):
        raise HTTPException(status_code=400, detail="Invalid storage name")

    file_path = storage_path / storage_name

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    if size == "thumbnail":
        thumb = get_thumbnail(file_path)

        return StreamingResponse(
            thumb,
            media_type="image/jpeg"
        )

    return FileResponse(
        path=file_path,
        media_type="image/png",
        content_disposition_type="inline"
    )

@router.get("/files")
async def get_files():
    files = await file_services.get_files()
    return files