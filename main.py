from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes import home, home_photos, home_clips, telemetry, docs, file
from contextlib import asynccontextmanager
from db import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(docs.router)
app.include_router(home.router)
app.include_router(home_photos.router)
app.include_router(home_clips.router)
app.include_router(telemetry.router)
app.include_router(file.router)