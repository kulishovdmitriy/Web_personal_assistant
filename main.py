import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def start_app():
    return {"massage": "Hello FastAPI"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
