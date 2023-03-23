from typing import Optional

from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models.network_game_audit import NetworkGameAudit
from app.schemas import PagedResult
from app.schemas.network_game_audit import NetworkGameAuditCreate, NetworkGameAuditUpdate


class CRUDNetworkGameAudit(CRUDBase[NetworkGameAudit, NetworkGameAuditCreate, NetworkGameAuditUpdate]):
    def create(self, db: Session, *, obj_in: NetworkGameAudit) -> NetworkGameAudit:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_paged_network_games_audits(self, db: Session, query_str: Optional[str], skip: int = 0,
                                       limit: int = 10) -> PagedResult:
        query = db.query(NetworkGameAudit)
        if query_str:
            query = query.filter(models.NetworkGameAudit.title.like(f"%{query_str}%")
                                 or models.NetworkGameAudit.publisher.like(f"%{query_str}%")
                                 or models.NetworkGameAudit.operator.like(f"%{query_str}%"))

        audits = query.offset(skip).limit(limit).all()
        total_count = query.count()
        return PagedResult(total_count=total_count, data=audits)

    def get_all(self, db: Session) -> list[NetworkGameAudit]:
        return db.query(NetworkGameAudit).order_by(NetworkGameAudit.publish_date.desc()).all()

    def multiple_create(self, db: Session, *, objs_in: list[NetworkGameAudit]) -> None:
        db.add_all(objs_in)
        db.commit()

    # def get_latest_date(self, db: Session) -> datetime.datetime:
    #     """获取最新发布日期"""
    #     return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        """删除所有数据"""
        db.query(NetworkGameAudit).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(NetworkGameAudit).first() else True


network_game_audit = CRUDNetworkGameAudit(NetworkGameAudit)
