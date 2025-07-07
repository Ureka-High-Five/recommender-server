# app/settings/local.py

from pydantic_settings import BaseSettings

class LocalSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    W2V_MODEL_PATH: str
    RECOMMEND_CONTENTS_COUNT: int

    class Config:
        env_file = ".env.local"


settings = LocalSettings()
