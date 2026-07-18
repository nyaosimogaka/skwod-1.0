# app/api/v1/person_team.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.person_team import PersonTeam
from app.schemas.person_team import PersonTeamCreate, PersonTeamResponse, PersonTeamUpdate

router = APIRouter(prefix="/person-teams", tags=["person-teams"])


@router.get("/", response_model=list[PersonTeamResponse])
async def list_person_teams(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonTeam))
    return result.scalars().all()


@router.get("/{pt_id}", response_model=PersonTeamResponse)
async def get_person_team(pt_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonTeam).where(PersonTeam.pt_id == pt_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="PersonTeam not found")
    return obj


@router.post("/", response_model=PersonTeamResponse)
async def add_person_team(payload: PersonTeamCreate, db: AsyncSession = Depends(get_db)):
    new_obj = PersonTeam(
        team_id=payload.team_id,
        person_id=payload.person_id,
        person_type=payload.person_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        transfer_reason=payload.transfer_reason,
        status=payload.status,
        pt_pic=payload.pt_pic,
    )
    db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj


@router.put("/{pt_id}", response_model=PersonTeamResponse)
async def update_person_team(pt_id: str, payload: PersonTeamUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonTeam).where(PersonTeam.pt_id == pt_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="PersonTeam not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{pt_id}", status_code=204)
async def delete_person_team(pt_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonTeam).where(PersonTeam.pt_id == pt_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="PersonTeam not found")
    await db.delete(obj)
    await db.commit()
    return None
