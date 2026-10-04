from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "THE GARAGE SERVER HAS ACHIEVED SENTIENCE. DO NOT UNPLUG IT."
    }