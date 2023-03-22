import datetime
from typing import Optional

from pydantic import BaseModel


class EGameAuditBase(BaseModel):
    name: str
    publisher: str
    audit_no: str
    publish_date: str


class EGameAuditCreate(EGameAuditBase):
    pass


class EGameAuditUpdate(EGameAuditBase):
    pass


class EGameAuditInDBBase(EGameAuditBase):
    id: int
    name: str
    publisher: str
    audit_no: str
    publish_date: str

    class Config:
        orm_mode = True


class EGameAudit(EGameAuditInDBBase):
    pass
