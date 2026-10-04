from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "TEST THE GARAGE SERVER HAS ACHIEVED SENTIENCE. DO NOT UNPLUG IT."
    }