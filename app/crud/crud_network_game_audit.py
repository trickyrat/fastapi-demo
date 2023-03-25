from typing import Optional

from sqlalchemy import or_, text, func, case, literal_column
from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.models.network_game_audit import NetworkGameAudit
from app.schemas import PagedResult
from app.schemas.network_game_audit import (
    NetworkGameAuditCreate,
    NetworkGameAuditUpdate,
    NetworkGameCategoryRank,
)


class CRUDNetworkGameAudit(
    CRUDBase[NetworkGameAudit, NetworkGameAuditCreate, NetworkGameAuditUpdate]
):
    def create(self, db: Session, *, obj_in: NetworkGameAudit) -> NetworkGameAudit:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_paged_network_games_audits(
            self, db: Session, query_str: Optional[str], skip: int = 0, limit: int = 10
    ) -> PagedResult:
        query = db.query(NetworkGameAudit)
        if query_str:
            query = query.filter(or_(
                models.NetworkGameAudit.name.like(f"%{query_str}%"),
                models.NetworkGameAudit.publisher.like(f"%{query_str}%"),
                models.NetworkGameAudit.operator.like(f"%{query_str}%"))
            )

        audits = query.offset(skip).limit(limit).all()
        total_count = query.count()
        return PagedResult(total_count=total_count, data=audits)

    def get_all(self, db: Session) -> list[NetworkGameAudit]:
        return (
            db.query(NetworkGameAudit)
            .order_by(NetworkGameAudit.publish_date.desc())
            .all()
        )

    def multiple_create(self, db: Session, *, objs_in: list[NetworkGameAudit]) -> None:
        db.add_all(objs_in)
        db.commit()

    # def get_latest_date(self, db: Session) -> datetime.datetime:
    #     """获取最新发布日期"""
    #     return db.query(NPPATable).order_by(NPPATable.publish_date.desc()).first().publish_date

    def delete_all(self, db: Session) -> None:
        db.query(NetworkGameAudit).delete()
        db.commit()

    def is_empty(self, db: Session) -> bool:
        return False if db.query(NetworkGameAudit).first() else True

    def get_audit_category_top_10(
            self, db: Session, category: Optional[int]
    ) -> NetworkGameCategoryRank:
        """Get the top 10 audit category
        :param category: the category of game e.g: 1: domestic 2: foreign
        """

        query = db.query(case(
            (NetworkGameAudit.audit_category == '', literal_column("'无分类'")),
            else_=NetworkGameAudit.audit_category
        ).label('audit_category'), func.count(text('*')).label('audit_count'))
        if category:
            query = query.filter(NetworkGameAudit.category == category)

        result_proxy = query.group_by(NetworkGameAudit.audit_category).order_by(text('audit_count desc')).limit(
            10).all()
        rank = NetworkGameCategoryRank(audit_categories=[], audit_counts=[])
        for item in result_proxy:
            rank.audit_categories.append(item[0])
            rank.audit_counts.append(item[1])
        return rank


network_game_audit = CRUDNetworkGameAudit(NetworkGameAudit)
