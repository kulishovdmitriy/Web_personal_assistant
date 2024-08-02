import re
import uvicorn
import aioredis

from pathlib import Path
from ipaddress import ip_address
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Callable
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter

from src.database.user_db import get_database
from src.routers import contacts, auth, tracing_system_email, avatar_user
from src.conf.config import settings

origins = ["*"]  # Мы определяем список доменов, которые могут отправлять запросы в наш API

banned_ips = [ip_address("192.168.0.1"), ip_address("192.168.1.1")]


user_agent_ban_list = [r"Googlebot", r"Python-urllib"]


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


@app.middleware("http")
async def ban_ips(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip in banned_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response


@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response

BASE_DIR = Path(".")
app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")

app.include_router(auth.router)
app.include_router(contacts.router, prefix="/api")
app.include_router(tracing_system_email.router, prefix="/users")
app.include_router(avatar_user.router, prefix="/api/users")


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
