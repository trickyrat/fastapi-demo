import datetime
from typing import Optional

from pydantic import BaseModel


class NPPATableBase(BaseModel):
    title: str
    url: str
    publish_date:  str


class NPPATableCreate(NPPATableBase):
    pass


class NPPATableUpdate(NPPATableBase):
    pass


class NPPATableInDBBase(NPPATableBase):
    id: int
    title: str
    url: str
    publish_date: datetime.datetime

    class Config:
        orm_mode = True


class NPPATable(NPPATableInDBBase):
    pass
