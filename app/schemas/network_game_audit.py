import datetime
from typing import Optional

from pydantic import BaseModel


class NetworkGameAuditBase(BaseModel):
    name: str
    audit_category: str
    publisher: str
    operator: str
    audit_no: str
    isbn: str
    category: str
    publish_date: str


class NetworkGameAuditCreate(NetworkGameAuditBase):
    pass


class NetworkGameAuditUpdate(NetworkGameAuditBase):
    pass


class NetworkGameAuditInDBBase(NetworkGameAuditBase):
    id: int
    name: str
    audit_category: str
    publisher: str
    operator: str
    audit_no: str
    isbn: str
    category: str
    publish_date: str

    class Config:
        orm_mode = True


class NetworkGameAudit(NetworkGameAuditInDBBase):
    pass
