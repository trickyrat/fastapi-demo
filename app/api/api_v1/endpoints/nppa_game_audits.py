from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.PagedResult)
async def read_game_audits(
        *,
        db: Session = Depends(deps.get_db),
        title: Optional[str] = None,
        skip: int = 0,
        limit: int = 10
) -> Any:
    return crud.game_audit.get_paged_audits(db, title=title, skip=skip, limit=limit)


@router.get("/{audit_id}", response_model=schemas.GameAudit)
async def get_audit(
        *,
        db: Session = Depends(deps.get_db),
        audit_id: int):
    return crud.game_audit.get(db, audit_id)
