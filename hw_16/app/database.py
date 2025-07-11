from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/app"

engine = create_async_engine(DATABASE_URL, echo=True)
