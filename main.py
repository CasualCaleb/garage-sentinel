from fastapi import FastAPI
from routes import home, telemetry

app = FastAPI()

app.include_router(home.router)
app.include_router(telemetry.router)