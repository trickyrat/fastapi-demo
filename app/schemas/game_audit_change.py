from pydantic import BaseModel


class GameAuditChangeBase(BaseModel):
    name: str
    audit_category: str
    publisher: str
    operator: str
    cancel_msg: str
    audit_no: str
    isbn: str
    approve_date: str


class GameAuditChangeCreate(GameAuditChangeBase):
    pass


class GameAuditChangeUpdate(GameAuditChangeBase):
    pass


class GameAuditChangeInDBBase(GameAuditChangeBase):
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


class GameAuditChange(GameAuditChangeInDBBase):
    pass
