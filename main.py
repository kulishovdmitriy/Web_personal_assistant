import uvicorn
from fastapi import FastAPI

from src.routers import contacts, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(contacts.router, prefix="/api")


@app.get("/")
async def start_app():
    return {"massage": "Hello FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
