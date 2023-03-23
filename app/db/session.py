from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if settings.DATABASE == 'mysql':
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI, 
        future=True
    )
else:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI, 
        connect_args={'check_same_thread': False},
        future=True
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
