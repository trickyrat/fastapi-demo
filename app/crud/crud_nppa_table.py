import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.nppa_table import NPPATable
from app.schemas.nppa_table import NPPATableCreate, NPPATableUpdate


class CRUDNPPATable(CRUDBase[NPPATable, NPPATableCreate, NPPATableUpdate]):
    def create(self, db: Session, *, obj_in: NPPATable) -> NPPATable:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all(self, db: Session) -> list[NPPATable]:
        return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).all()

    def multiple_create(self, db: Session, *, objs_in: list[NPPATable]) -> None:
        db.add_all(objs_in)
        db.commit()

    def get_latest_date(self, db: Session) -> datetime.datetime:
        """获取最新发布日期"""
        return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        """删除所有数据"""
        db.query(NPPATable).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(NPPATable).first() else True


nppa_table = CRUDNPPATable(NPPATable)
