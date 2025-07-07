# app/settings/__init__.py
import os
from .local import LocalSettings

env = os.getenv("ENV", "local") # 기본 설정을 local로

Settings = LocalSettings
settings = Settings()