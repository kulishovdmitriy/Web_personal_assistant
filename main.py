import uvicorn
from fastapi import FastAPI

from src.routers import users

app = FastAPI()

app.include_router(users.router, prefix="/api")


@app.get("/")
async def start_app():
    return {"massage": "Hello FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
