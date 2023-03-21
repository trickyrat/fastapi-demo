import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.nppa_table import NPPATable


class CRUDNPPATable(CRUDBase[NPPATable]):
    def create(self, db: Session, *, obj_in: NPPATable) -> NPPATable:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def multiple_create(self, db: Session, *, objs_in: list(NPPATable)) -> None:
        db.add_all(objs_in)
        db.commit()

    def get_latest_date(self, db: Session) -> datetime.datetime:
        return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first()


nppa_table = CRUDNPPATable(NPPATable)
