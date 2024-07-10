from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.conf.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, aoflush=False)


async def get_database():
    async with async_session() as session:
        yield session
