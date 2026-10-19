import aiosqlite
from pathlib import Path
from contextlib import asynccontextmanager

DATABASE_PATH = Path(__file__).parent / 'database.db'

@asynccontextmanager
async def get_connection():
    async with aiosqlite.connect(DATABASE_PATH) as conn:
        yield conn