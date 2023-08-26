# coding=utf-8

import os
import secrets
from typing import Optional
import yaml

from pydantic import BaseSettings

base_dir = os.path.abspath(os.path.dirname("main"))


with open("appsettings.yaml", "r", encoding="u8") as file:
    data = yaml.safe_load(file)


class Settings(BaseSettings):
    API_BASE_URL: str = f"{data['api_base_url']}/{data['api_version']}"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    MYSQL_CONNECTION_STRING: Optional[str] \
        = f"mysql+pymysql://{data['mysql']['user_name']}:{data['mysql']['password']}@{data['mysql']['server']}:" \
          f"{data['mysql']['port']}/{data['mysql']['database']}?charset=utf8"
    SQLSERVER_CONNECTION_STRING: Optional[str] \
        = f"mssql+pymssql://{data['sqlserver']['user_name']}:{data['sqlserver']['password']}@" \
          f"{data['sqlserver']['server']}:{data['sqlserver']['port']}/{data['sqlserver']['database']}?charset=utf8"
    ORIGINS: list[str] = data['cors_origins']
    DATABASE: Optional[str] = data['database']
    NPPA_BASE_URL: Optional[str] = data['nppa']['base_url']
    NPPA_DATA_URL: Optional[str] = data['nppa']['data_url']
    NPPA_SUFFIX: Optional[str] = data['nppa']['suffix']


settings = Settings()
