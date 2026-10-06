from fastapi import APIRouter, HTTPException
from pathlib import Path

THERMAL_ZONE = Path("/sys/class/thermal/thermal_zone0/temp")

router = APIRouter()

@router.get("/api/temp")
async def get_cpu_temp():
    try:
        raw_temp = THERMAL_ZONE.read_text().strip()
        temp_c = int(raw_temp) / 1000

        return {
            "cpu_temp_c": round(temp_c, 1)
        }

    except (FileNotFoundError, ValueError, PermissionError):
        raise HTTPException(
            status_code=500,
            detail="Unable to read CPU temperature"
        )