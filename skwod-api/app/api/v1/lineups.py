# app/api/v1/lineups.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.session import get_db
from app.models.lineups import Lineup
from app.schemas.lineups import LineupCreate, LineupResponse, LineupUpdate

router = APIRouter(prefix="/lineups", tags=["lineups"])


@router.get("/", response_model=list[LineupResponse])
async def list_lineups(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lineup))
    return result.scalars().all()


@router.post("/", response_model=LineupResponse)
async def create_lineup(payload: LineupCreate, db: AsyncSession = Depends(get_db)):
    new_lineup = Lineup(**payload.model_dump())
    db.add(new_lineup)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Could not create lineup")
    await db.refresh(new_lineup)
    return new_lineup


@router.put("/{game_id}/{team_id}/{person_id}", response_model=LineupResponse)
async def update_lineup(
    game_id: str,
    team_id: str,
    person_id: str,
    payload: LineupUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Lineup).where(
        and_(
            Lineup.game_id == game_id,
            Lineup.team_id == team_id,
            Lineup.person_id == person_id,
        )
    )
    result = await db.execute(stmt)
    lineup = result.scalar_one_or_none()
    if lineup is None:
        raise HTTPException(status_code=404, detail="Lineup not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(lineup, field, value)

    await db.commit()
    await db.refresh(lineup)
    return lineup


@router.delete("/{game_id}/{team_id}/{person_id}", status_code=204)
async def delete_lineup(game_id: str, team_id: str, person_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Lineup).where(
        and_(
            Lineup.game_id == game_id,
            Lineup.team_id == team_id,
            Lineup.person_id == person_id,
        )
    )
    result = await db.execute(stmt)
    lineup = result.scalar_one_or_none()
    if lineup is None:
        raise HTTPException(status_code=404, detail="Lineup not found")
    await db.delete(lineup)
    await db.commit()
    return None
