from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",         
        env_file_encoding="utf-8"
    )

    database_url: str
    secret_key: str
    redis_host: str = "localhost"
    redis_port: int = 6379

settings = Settings()
