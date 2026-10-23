import asyncio
from db.database import delete_expired_registrations

async def registration_cleanup_tool():
    while True:
        await delete_expired_registrations()
        await asyncio.sleep(1)