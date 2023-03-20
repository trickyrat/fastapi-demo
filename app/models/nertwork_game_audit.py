import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.db.base_class import Base


class NetworkGameAudit(Base):
    # def __init__(self, name: str, category: str, publisher: str, operator: str, audit_no: str, isbn: str, publish_date: str):
    #     self.name = name
    #     self.category = category
    #     self.publisher = publisher
    #     self.operator = operator
    #     self.audit_no = audit_no
    #     self.isbn = isbn
    #     self.publish_date = datetime.datetime.strptime(publish_date, "%Y-%m-%d")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, index=True)
    audit_category = Column(String(128), unique=True, index=True)
    publisher = Column(String(512), unique=False, index=True)
    operator = Column(String(512), unique=False, index=True)
    audit_no = Column(String(128), unique=True, index=True)
    isbn = Column(String(128), unique=True, index=True)
    category = Column(Integer, unique=False, index=True) # 1 国产 2 进口
    publish_date = Column(DateTime)
