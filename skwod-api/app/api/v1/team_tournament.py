# app/api/v1/team_tournament.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.team_tournament import TeamTournament
from app.schemas.team_tournament import (
    TeamTournamentCreate,
    TeamTournamentResponse,
    TeamTournamentUpdate,
)

router = APIRouter(prefix="/team-tournaments", tags=["team-tournaments"])


@router.get("/", response_model=list[TeamTournamentResponse])
async def list_team_tournaments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TeamTournament))
    return result.scalars().all()


@router.get("/{tt_id}", response_model=TeamTournamentResponse)
async def get_team_tournament(tt_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TeamTournament).where(TeamTournament.tt_id == tt_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="TeamTournament not found")
    return obj


@router.post("/", response_model=TeamTournamentResponse)
async def add_team_tournament(payload: TeamTournamentCreate, db: AsyncSession = Depends(get_db)):
    new_obj = TeamTournament(team_id=payload.team_id, tournament_id=payload.tournament_id)
    db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj


@router.put("/{tt_id}", response_model=TeamTournamentResponse)
async def update_team_tournament(tt_id: str, payload: TeamTournamentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TeamTournament).where(TeamTournament.tt_id == tt_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="TeamTournament not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{tt_id}", status_code=204)
async def delete_team_tournament(tt_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TeamTournament).where(TeamTournament.tt_id == tt_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="TeamTournament not found")
    await db.delete(obj)
    await db.commit()
    return None
