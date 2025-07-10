# app/settings/__init__.py
from .local import LocalSettings

Settings = LocalSettings
settings = Settings()