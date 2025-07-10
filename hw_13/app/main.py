from fastapi import FastAPI
from app.routes import notes
from app.redis_cache import redis_cache
from app.init_db import create_db_and_tables
from app.utils.wait_for_db import wait_for_postgres
import os
from app.database import SessionLocal
from app.models import User

app = FastAPI()

@app.on_event("startup")
async def startup():
    print("DB_HOST:", os.getenv("DB_HOST", "db"))
    print("DB_PORT:", os.getenv("DB_PORT", "5432"))
    print("DB_NAME:", os.getenv("DB_NAME", "app"))
    print("DB_USER", os.getenv("DB_USER", "postgres"))
    print("DB_PASSWORD:", os.getenv("DB_PASSWORD", "password"))
    wait_for_postgres(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        db=os.getenv("DB_NAME", "app"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password")
    )
    create_db_and_tables()
    # Добавить тестового пользователя, если его нет
    db = SessionLocal()
    if not db.query(User).filter_by(id=1).first():
        db.add(User(id=1, username="testuser"))
        db.commit()
    db.close()
    await redis_cache.connect()

@app.on_event("shutdown")
async def shutdown():
    await redis_cache.disconnect()

app.include_router(notes.router)
