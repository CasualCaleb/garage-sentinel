from pathlib import Path
from db.connection import get_connection
from models import File

schema_path = Path(__file__).parent / "schema.sql"

async def init_db():
    async with get_connection() as conn:
        await conn.executescript(schema_path.read_text())

async def add_file(filename: str, storage_name: str) -> int:
    async with get_connection() as conn:
        cursor = await conn.execute("""
            INSERT INTO files (filename, storage_name)
            VALUES (?, ?)
            RETURNING id
        """, (filename, storage_name)
        )

        row = await cursor.fetchone()

        await conn.commit()

        return row

async def get_files() -> list[File]:
    async with get_connection() as conn:
        cursor = await conn.execute("""
            SELECT *
            FROM files
        """)

        files = [
            File(
                id=row[0],
                filename=row[1],
                storage_name=row[2],
                created_at=row[3],
            )
            for row in await cursor.fetchall()
        ]

        return files

async def get_file_by_storage_name(storage_name: str) -> File:
    async with get_connection() as conn:
        cursor = await conn.execute("""
            SELECT *
            FROM files
            WHERE storage_name = ?
            VALUES (?)
        """, (storage_name,)
        )

        row = await cursor.fetchone()

        return File(
            id=row[0],
            filename=row[1],
            storage_name=row[2],
            created_at=row[3],
        )