from fastapi import FastAPI
from routes import home, telemetry, docs

app = FastAPI()

app.include_router(docs.router)
app.include_router(home.router)
app.include_router(telemetry.router)