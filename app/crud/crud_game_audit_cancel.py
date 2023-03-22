from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.game_audit_cancel import GameAuditCancel
from app.schemas.game_audit_cancel import GameAuditCancelCreate, GameAuditCancelUpdate


class CRUDGameAuditCancel(CRUDBase[GameAuditCancel, GameAuditCancelCreate, GameAuditCancelUpdate]):
    def create(self, db: Session, *, obj_in: GameAuditCancel) -> GameAuditCancel:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all(self, db: Session) -> list[GameAuditCancel]:
        return db.query(GameAuditCancel).order_by(GameAuditCancel.publish_date.desc()).all()

    def multiple_create(self, db: Session, *, objs_in: list[GameAuditCancel]) -> None:
        db.add_all(objs_in)
        db.commit()

    # def get_latest_date(self, db: Session) -> datetime.datetime:
    #     """获取最新发布日期"""
    #     return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        """删除所有数据"""
        db.query(GameAuditCancel).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(GameAuditCancel).first() else True


game_audit_cancel = CRUDGameAuditCancel(GameAuditCancel)
