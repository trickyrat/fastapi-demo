from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

mysql_engine = create_engine(
    settings.MYSQL_CONNECTION_STRING,
    future=True
    # echo=True
)

sqlserver_engine = create_engine(
    settings.SQLSERVER_CONNECTION_STRING,
    future=True
    # echo=True
)

MysqlSession = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine, future=True)
SqlServerSession = sessionmaker(autocommit=False, autoflush=False, bind=sqlserver_engine, future=True)
