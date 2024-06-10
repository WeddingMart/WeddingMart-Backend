# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

user = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
database = os.environ["DB_NAME"]

# Retrieve variables from the environment
DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as session:
        yield session
