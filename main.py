import uvicorn
import aioredis
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter

from src.database.user_db import get_database
from src.routers import contacts, auth, static
from src.conf.config import settings

origins = ["*"]  # Мы определяем список доменов, которые могут отправлять запросы в наш API


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    redis_db = await aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(redis_db)

    yield

    await redis_db.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth.router)
app.include_router(contacts.router, prefix="/api")
app.include_router(static.router, prefix="/users")


@app.get("/")
async def start_app():
    return {"message": "Hello FastAPI"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_database)):
    try:

        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "DataBase is connect!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
