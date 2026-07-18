# app/api/v1/person_participation.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.person_participation import PersonParticipation
from app.schemas.person_participation import (
    PersonParticipationCreate,
    PersonParticipationResponse,
    PersonParticipationUpdate,
)

router = APIRouter(prefix="/person-participations", tags=["person-participations"])


@router.get("/", response_model=list[PersonParticipationResponse])
async def list_person_participations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonParticipation))
    return result.scalars().all()


@router.get("/{pp_id}", response_model=PersonParticipationResponse)
async def get_person_participation(pp_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonParticipation).where(PersonParticipation.pp_id == pp_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="PersonParticipation not found")
    return obj


@router.post("/", response_model=PersonParticipationResponse)
async def add_person_participation(payload: PersonParticipationCreate, db: AsyncSession = Depends(get_db)):
    new_obj = PersonParticipation(pt_id=payload.pt_id, tt_id=payload.tt_id, pp_pic=payload.pp_pic)
    db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj


@router.put("/{pp_id}", response_model=PersonParticipationResponse)
async def update_person_participation(pp_id: str, payload: PersonParticipationUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonParticipation).where(PersonParticipation.pp_id == pp_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="PersonParticipation not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{pp_id}", status_code=204)
async def delete_person_participation(pp_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonParticipation).where(PersonParticipation.pp_id == pp_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="PersonParticipation not found")
    await db.delete(obj)
    await db.commit()
    return None
