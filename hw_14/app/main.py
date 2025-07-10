from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/config")
def read_config():
    return {
        "database_url":settings.database_url,
        "secret_key":settings.secret_key,
        "redis_host":settings.redis_host,
        "redis_port":settings.redis_port,
    }