import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import contacts, auth, static

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth.router)
app.include_router(contacts.router, prefix="/api")
app.include_router(static.router, prefix="/users")


@app.get("/")
async def start_app():
    return {"massage": "Hello FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
