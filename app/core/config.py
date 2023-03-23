import platform
import secrets
from typing import Optional

from pydantic import BaseSettings

is_windows = platform.platform().startswith("Windows")


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SQLALCHEMY_DATABASE_URI: Optional[str] = \
        "mysql+pymysql://root:trickyrat@localhost:3306/test?charset=utf8" \
        if is_windows else "sqlite:///../../test.db"


settings = Settings()
