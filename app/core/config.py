import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator, AnyHttpUrl, HttpUrl


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql://user:root;password:trickyrat/db"


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    #
    # PROJECT_NAME: str
    # SENTRY_DSN: Optional[HttpUrl] = None
    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    #SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///./sql_app.db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = "mysql+pymysql://root:trickyrat@localhost:3306/test?charset=utf8"

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )


settings = Settings()
