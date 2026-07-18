"""
App settings using Pydantic V2 and pydantic_settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PATH: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=f".env.{ENV}")

settings = Settings()
