from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class LocalSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    W2V_MODEL_PATH: str
    RABBITMQ_URL: str
    RABBITMQ_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    MONGO_URL: str

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env.local"),
        env_file_encoding="utf-8"
    )

settings = LocalSettings()