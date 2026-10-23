from contextlib import asynccontextmanager
from tasks.cleanup import registration_cleanup_tool
from db import database
from fastapi import FastAPI
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()

    cleanup_task = asyncio.create_task(
        registration_cleanup_tool()
    )

    try:
        yield
    finally:
        cleanup_task.cancel()

        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass