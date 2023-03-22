import datetime
from typing import Optional

from pydantic import BaseModel


class AuditChangeBase(BaseModel):
    name: str
    audit_category: str
    publisher: str
    operator: str
    cancel_msg: str
    audit_no: str
    isbn: str
    approve_date: str


class AuditChangeCreate(AuditChangeBase):
    pass


class AuditChangeUpdate(AuditChangeBase):
    pass


class AuditChangeInDBBase(AuditChangeBase):
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


class AuditChange(AuditChangeInDBBase):
    pass
