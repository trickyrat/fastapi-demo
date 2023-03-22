import datetime
from typing import Optional

from pydantic import BaseModel


class AuditCancelBase(BaseModel):
    name: str
    audit_category: str
    publisher: str
    operator: str
    cancel_msg: str
    audit_no: str
    isbn: str
    approve_date: str


class AuditCancelCreate(AuditCancelBase):
    pass


class AuditCancelUpdate(AuditCancelBase):
    pass


class AuditCancelInDBBase(AuditCancelBase):
    id: int
    name: str
    audit_category: str
    publisher: str
    operator: str
    cancel_msg: str
    audit_no: str
    isbn: str
    approve_date: str

    class Config:
        orm_mode = True


class AuditCancel(AuditCancelInDBBase):
    pass
