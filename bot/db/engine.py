from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings
from db.models import Base
# Base = declarative_base()


DATABASE_URL = settings.DB_CONN_URL
try:
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(bind=engine, class_=AsyncSession)
except Exception as e:
    print(e)


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)