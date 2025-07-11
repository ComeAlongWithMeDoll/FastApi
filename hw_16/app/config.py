from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")  # обязательно прописать env

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
