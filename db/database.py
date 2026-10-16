from pathlib import Path
from db.connection import get_connection
from models import File

schema_path = Path(__file__).parent / "schema.sql"

async def init_db():
    async with get_connection() as conn:
        await conn.executescript(schema_path.read_text())

async def add_file(filename: str, filetype: str, storage_name: str) -> int:
    async with get_connection() as conn:
        cursor = await conn.execute("""
            INSERT INTO files (filename, filetype, storage_name)
            VALUES (?, ?, ?)
            RETURNING id
        """, (filename, filetype, storage_name)
        )

        row = await cursor.fetchone()

        await conn.commit()

        return row

async def get_files(filetypes: list[str] | None = None) -> list[File]:
    async with get_connection() as conn:
        query = "SELECT * FROM files"
        params = []

        if filetypes:
            placeholders = ", ".join("?" for _ in filetypes)
            query += f" WHERE LOWER(filetype) IN ({placeholders})"
            params = [ext.lower() for ext in filetypes]

        cursor = await conn.execute(query, params)

        files = [
            File(
                id=row[0],
                filename=row[1],
                filetype=row[2],
                storage_name=row[3],
                created_at=row[4],
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
        """, (storage_name,)
        )

        row = await cursor.fetchone()

        return File(
            id=row[0],
            filename=row[1],
            filetype=row[2],
            storage_name=row[3],
            created_at=row[4],
        )