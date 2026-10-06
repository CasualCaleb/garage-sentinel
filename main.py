from pathlib import Path
from fastapi import FastAPI
from routes import home, telemetry

app = FastAPI()

THERMAL_ZONE = Path("/sys/class/thermal/thermal_zone0/temp")

app.include_router(home.router)
app.include_router(telemetry.router)