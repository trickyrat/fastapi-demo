from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class GameAuditChange(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    audit_category = Column(String(128))
    publisher = Column(String(512))
    operator = Column(String(512))
    change_msg = Column(String(2048))
    audit_no = Column(String(128))
    isbn = Column(String(128))
    change_date = Column(DateTime)
