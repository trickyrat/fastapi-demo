from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class GameRevocationAudit(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    audit_category = Column(String(128))
    publisher = Column(String(512))
    operator = Column(String(512))
    revocation_msg = Column(String(2048))
    audit_no = Column(String(128))
    isbn = Column(String(128))
    approval_date = Column(DateTime)