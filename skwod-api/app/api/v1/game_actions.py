# app/api/v1/game_actions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import time

from app.db.session import get_db
from app.models.game_actions import GameActions
from app.schemas.game_actions import (
    GameActionsCreate,
    GameActionsResponse,
    GameActionsUpdate,
)

router = APIRouter(prefix="/game-actions", tags=["game-actions"])


@router.get("/", response_model=list[GameActionsResponse])
async def list_game_actions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GameActions))
    return result.scalars().all()


@router.post("/", response_model=GameActionsResponse)
async def create_game_action(payload: GameActionsCreate, db: AsyncSession = Depends(get_db)):
    new_action = GameActions(**payload.model_dump())
    db.add(new_action)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Could not create game action")
    await db.refresh(new_action)
    return new_action


@router.put("/{game_id}/{team_id}/{person_id}/{action_id}/{shot_clock}", response_model=GameActionsResponse)
async def update_game_action(
    game_id: str,
    team_id: str,
    person_id: str,
    action_id: str,
    shot_clock: str,  # ISO time string expected (e.g., "00:24:00")
    payload: GameActionsUpdate,
    db: AsyncSession = Depends(get_db),
):
    # parse shot_clock string -> time object is done by DB/driver if necessary
    stmt = select(GameActions).where(
        and_(
            GameActions.game_id == game_id,
            GameActions.team_id == team_id,
            GameActions.person_id == person_id,
            GameActions.action_id == action_id,
            GameActions.shot_clock == shot_clock,
        )
    )
    result = await db.execute(stmt)
    ga = result.scalar_one_or_none()
    if ga is None:
        raise HTTPException(status_code=404, detail="Game action not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(ga, field, value)

    await db.commit()
    await db.refresh(ga)
    return ga


@router.delete("/{game_id}/{team_id}/{person_id}/{action_id}/{shot_clock}", status_code=204)
async def delete_game_action(
    game_id: str,
    team_id: str,
    person_id: str,
    action_id: str,
    shot_clock: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(GameActions).where(
        and_(
            GameActions.game_id == game_id,
            GameActions.team_id == team_id,
            GameActions.person_id == person_id,
            GameActions.action_id == action_id,
            GameActions.shot_clock == shot_clock,
        )
    )
    result = await db.execute(stmt)
    ga = result.scalar_one_or_none()
    if ga is None:
        raise HTTPException(status_code=404, detail="Game action not found")
    await db.delete(ga)
    await db.commit()
    return None
