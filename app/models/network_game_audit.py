import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.db.base_class import Base


class NetworkGameAudit(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    audit_category = Column(String(128))
    publisher = Column(String(512))
    operator = Column(String(512))
    audit_no = Column(String(128))
    isbn = Column(String(128))
    category = Column(Integer)  # 1 国产 2 进口
    publish_date = Column(DateTime)
