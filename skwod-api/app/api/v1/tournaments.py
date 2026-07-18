from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.tournaments import Tournament
from app.schemas.tournaments import (
    TournamentCreate,
    TournamentUpdate,
    TournamentResponse,
)

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


# ------------------------
# GET all tournaments
# ------------------------
@router.get("/", response_model=list[TournamentResponse])
async def list_tournaments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tournament))
    return result.scalars().all()


# ------------------------
# GET tournament by ID
# ------------------------
@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tournament).where(Tournament.tournament_id == tournament_id)
    )
    tournament = result.scalar_one_or_none()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return tournament


# ------------------------
# CREATE new tournament
# ------------------------
@router.post("/", response_model=TournamentResponse)
async def create_tournament(
    payload: TournamentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_tournament = Tournament(
        tournament_name=payload.tournament_name,
        season=payload.season,
        subcategory=payload.subcategory,
        parent_tournament_id=payload.parent_tournament_id,
        sport_id=payload.sport_id,
    )

    db.add(new_tournament)
    await db.commit()
    await db.refresh(new_tournament)

    return new_tournament


# ------------------------
# UPDATE tournament
# ------------------------
@router.put("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: str,
    payload: TournamentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Tournament).where(Tournament.tournament_id == tournament_id)
    )
    tournament = result.scalar_one_or_none()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    # partial update
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tournament, key, value)

    await db.commit()
    await db.refresh(tournament)

    return tournament


# ------------------------
# DELETE tournament
# ------------------------
@router.delete("/{tournament_id}")
async def delete_tournament(tournament_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tournament).where(Tournament.tournament_id == tournament_id)
    )
    tournament = result.scalar_one_or_none()

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    await db.delete(tournament)
    await db.commit()

    return {"message": "Tournament deleted successfully"}
