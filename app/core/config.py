from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Lender Backend"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "lender_db"
    POSTGRES_PORT: str = "5432"

    # Hatchet
    HATCHET_CLIENT_TOKEN: str = ""

    GOOGLE_PROJECT_ID: str = ""
    GOOGLE_PROJECT_LOCATION: str = ""

    # File Uploads
    UPLOAD_DIR: str = "uploads"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
