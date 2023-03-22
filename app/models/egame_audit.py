from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class EGameAudit(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    publisher = Column(String(512), index=True)
    audit_no = Column(String(128), index=True)
    publish_date = Column(DateTime)
