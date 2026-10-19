from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from db import database
from routes import (
    home, home_login, home_photos,
    home_clips, telemetry, docs,
    file, auth, users, admin
)
from config import SESSION_SECRET

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)

app.include_router(docs.router)
app.include_router(home.router)
app.include_router(home_login.router)
app.include_router(home_photos.router)
app.include_router(home_clips.router)
app.include_router(telemetry.router)
app.include_router(file.router)