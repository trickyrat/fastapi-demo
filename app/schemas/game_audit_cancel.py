import datetime
from typing import Optional

from pydantic import BaseModel


class GameAuditCancelBase(BaseModel):
    name: str
    audit_category: str
    publisher: str
    operator: str
    cancel_msg: str
    audit_no: str
    isbn: str
    approve_date: str


class GameAuditCancelCreate(GameAuditCancelBase):
    pass


class GameAuditCancelUpdate(GameAuditCancelBase):
    pass


class GameAuditCancelInDBBase(GameAuditCancelBase):
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


class GameAuditCancel(GameAuditCancelInDBBase):
    pass
