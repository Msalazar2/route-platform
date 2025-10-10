from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: AnyUrl = "postgresql+psycopg://route:routepw@localhost:5432/route"
    ENV: str = "dev"
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Route API"

    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

settings = Settings()
