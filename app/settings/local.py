from pydantic_settings import BaseSettings

# .env.local 설정 파일을 읽어와서 쉽게 접근할 수 있도록 해주는 인터페이스
class LocalSettings(BaseSettings):
    DB_URL: str
    DB_ECHO: bool
    DB_POOL_SIZE: int
    DB_POOL_RECYCLE: int

    class Config:
        env_file = ".env.local"
