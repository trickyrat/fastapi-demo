from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.game_audit_change import GameAuditChange
from app.schemas.game_audit_change import GameAuditChangeCreate, GameAuditChangeUpdate


class CRUDGameAuditChange(CRUDBase[GameAuditChange, GameAuditChangeCreate, GameAuditChangeUpdate]):
    def create(self, db: Session, *, obj_in: GameAuditChange) -> GameAuditChange:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_all(self, db: Session) -> list[GameAuditChange]:
        return db.query(GameAuditChange).order_by(GameAuditChange.publish_date.desc()).all()

    def multiple_create(self, db: Session, *, objs_in: list[GameAuditChange]) -> None:
        db.add_all(objs_in)
        db.commit()

    # def get_latest_date(self, db: Session) -> datetime.datetime:
    #     """获取最新发布日期"""
    #     return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        """删除所有数据"""
        db.query(GameAuditChange).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(GameAuditChange).first() else True


game_audit_change = CRUDGameAuditChange(GameAuditChange)
