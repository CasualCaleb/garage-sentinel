from pathlib import Path
from db.connection import get_connection
from models import File

schema_path = Path(__file__).parent / "schema.sql"

async def init_db():
    async with get_connection() as conn:
        await conn.executescript(schema_path.read_text())

async def add_file(user_id: int, filename: str, filetype: str, storage_name: str) -> int:
    async with get_connection() as conn:
        cursor = await conn.execute("""
            INSERT INTO files (user_id, filename, filetype, storage_name)
            VALUES (?, ?, ?, ?)
            RETURNING id
        """, (user_id, filename, filetype, storage_name)
        )

        row = await cursor.fetchone()

        await conn.commit()

        return row

async def get_files_by_user_id(user_id: int, filetypes: list[str] | None = None) -> list[File]:
    async with get_connection() as conn:
        query = "SELECT * FROM files"
        params = []

        query += " WHERE user_id = ?"
        params.append(user_id)

        if filetypes:
            placeholders = ",".join("?" for _ in filetypes)
            query += f" AND filetype IN ({placeholders})"
            params.extend(filetypes)

        cursor = await conn.execute(query, params)

        files = [
            File(
                id=row[0],
                user_id=row[1],
                filename=row[2],
                filetype=row[3],
                storage_name=row[4],
                created_at=row[5],
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
            user_id=row[1],
            filename=row[2],
            filetype=row[3],
            storage_name=row[4],
            created_at=row[5],
        )