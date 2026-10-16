import re
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import models.file as file_model
from db import database
from services import file_services
from services.file_services import storage_path, get_thumbnail

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
allowed_types = ["png", "jpg", "jpeg", "mp4"]

async def validate_file(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(400, "Missing filename")

    extension = file.filename.rsplit(".", 1)[-1].lower()

    if extension not in allowed_types:
        raise HTTPException(415, "Unsupported file format")

    if file.size is not None and file.size > MAX_FILE_SIZE:
        raise HTTPException(413, f"File too large")

    return extension

@router.post("/file", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename

    if not isinstance(filename, str):
        raise HTTPException(status_code=400, detail="Filename missing")

    file_type = await validate_file(file)
    data = await file.read()

    if not isinstance(data, bytes):
        raise HTTPException(status_code=400, detail="File is empty")

    file_id = await file_services.add_file(
        filename=filename,
        file_type=file_type,
        data= data
    )

    return {"id": file_id}

@router.get("/file/{storage_name}")
async def get_file(storage_name: str, size: str = "original"):
    if not re.fullmatch(r"[0-9a-f]{32}", storage_name):
        raise HTTPException(status_code=400, detail="Invalid storage name")

    file_path = storage_path / storage_name

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    file = await database.get_file_by_storage_name(storage_name)

    if not isinstance(file, file_model.File):
        raise HTTPException(status_code=404, detail="File not found")

    if file.filetype in ["mp4"]:
        return FileResponse(
            path=file_path,
            media_type="video/mp4",
            content_disposition_type="inline"
        )

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

@router.get("/photos")
async def get_photos():
    photos = await file_services.get_photos()
    return photos

@router.get("/videos")
async def get_videos():
    videos = await file_services.get_videos()
    return videos

@router.get("/clip/{storage_name}")
async def get_file(storage_name: str):
    file_path = storage_path / storage_name

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        content_disposition_type="inline"
    )