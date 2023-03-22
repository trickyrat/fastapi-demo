from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.audit_change import AuditChange
from app.schemas.audit_change import AuditChangeCreate, AuditChangeUpdate


class CRUDAuditChange(CRUDBase[AuditChange, AuditChangeCreate, AuditChangeUpdate]):
    def create(self, db: Session, *, obj_in: AuditChange) -> AuditChange:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all(self, db: Session) -> list[AuditChange]:
        return db.query(AuditChange).order_by(AuditChange.publish_date.desc()).all()

    def multiple_create(self, db: Session, *, objs_in: list[AuditChange]) -> None:
        db.add_all(objs_in)
        db.commit()

    # def get_latest_date(self, db: Session) -> datetime.datetime:
    #     """获取最新发布日期"""
    #     return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        """删除所有数据"""
        db.query(AuditChange).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(AuditChange).first() else True


audit_change = CRUDAuditChange(AuditChange)
