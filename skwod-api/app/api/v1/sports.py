from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.sports import Sport
from app.schemas.sports import SportCreate, SportResponse

router = APIRouter(prefix="/sports", tags=["sports"])


@router.get("/", response_model=list[SportResponse])
async def list_sports(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sport))
    sports = result.scalars().all()
    return sports


@router.post("/", response_model=SportResponse)
async def add_sport(payload: SportCreate, db: AsyncSession = Depends(get_db)):
    new_sport = Sport(sport_name=payload.sport_name)

    db.add(new_sport)
    await db.commit()
    await db.refresh(new_sport)

    return new_sport


# --------------------------------------------------------
# UPDATE SPORT
# --------------------------------------------------------
@router.put("/{sport_id}", response_model=SportResponse)
async def update_sport(
    sport_id: str,
    payload: SportCreate,
    db: AsyncSession = Depends(get_db)
):
    # Fetch existing record
    result = await db.execute(select(Sport).where(Sport.sport_id == sport_id))
    sport = result.scalar_one_or_none()

    if sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")

    # Update fields
    sport.sport_name = payload.sport_name

    await db.commit()
    await db.refresh(sport)

    return sport


# --------------------------------------------------------
# DELETE SPORT
# --------------------------------------------------------
@router.delete("/{sport_id}", status_code=204)
async def delete_sport(sport_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sport).where(Sport.sport_id == sport_id))
    sport = result.scalar_one_or_none()

    if sport is None:
        raise HTTPException(status_code=404, detail="Sport not found")

    await db.delete(sport)
    await db.commit()

    # No content returned (204)
    return None
