from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.audit_cancel import AuditCancel
from app.schemas.audit_cancel import AuditCancelCreate, AuditCancelUpdate


class CRUDAuditCancel(CRUDBase[AuditCancel, AuditCancelCreate, AuditCancelUpdate]):
    def create(self, db: Session, *, obj_in: AuditCancel) -> AuditCancel:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all(self, db: Session) -> list[AuditCancel]:
        return db.query(AuditCancel).order_by(AuditCancel.publish_date.desc()).all()

    def multiple_create(self, db: Session, *, objs_in: list[AuditCancel]) -> None:
        db.add_all(objs_in)
        db.commit()

    # def get_latest_date(self, db: Session) -> datetime.datetime:
    #     """获取最新发布日期"""
    #     return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        """删除所有数据"""
        db.query(AuditCancel).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(AuditCancel).first() else True


audit_cancel = CRUDAuditCancel(AuditCancel)
