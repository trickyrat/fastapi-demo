import os
import secrets
from typing import Optional

from pydantic import BaseSettings

base_dir = os.path.abspath(os.path.dirname("main"))
# db_dir = os.path.join(base_dir, "test.db")
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:5173",
    "https://localhost:5173",
]


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # SQLALCHEMY_DATABASE_URI: Optional[str] = "mysql+pymysql://root:trickyrat@localhost:3306/test?charset=utf8" if
    # is_windows else "sqlite:///" + db_dir
    SQLALCHEMY_DATABASE_URI: Optional[
        str
    ] = "mysql+pymysql://root:Trickyrat_05@localhost:3306/test?charset=utf8"
    # SQLALCHEMY_DATABASE_URI: Optional[str] = "mssql+pymssql://sa:trickyrat@localhost/Test"
    # DATABASE: str = "mysql"
    BASEDIR: Optional[str] = base_dir
    ORIGINS: list[str] = origins


settings = Settings()
