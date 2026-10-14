import aiosqlite
from pathlib import Path
from contextlib import asynccontextmanager

db_path = Path(__file__).parent / 'database.db'

@asynccontextmanager
async def get_connection():
    async with aiosqlite.connect(db_path) as conn:
        yield conn