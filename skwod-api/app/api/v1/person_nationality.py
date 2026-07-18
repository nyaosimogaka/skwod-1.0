from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.person_nationality import PersonNationality
from app.schemas.person_nationality import (
    PersonNationalityCreate,
    PersonNationalityResponse,
)

router = APIRouter(prefix="/person-nationality", tags=["person-nationality"])


# --------------------------------------------------------
# LIST ALL PERSON–COUNTRY LINKS
# --------------------------------------------------------
@router.get("/", response_model=list[PersonNationalityResponse])
async def list_links(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PersonNationality))
    links = result.scalars().all()
    return links


# --------------------------------------------------------
# CREATE LINK
# --------------------------------------------------------
@router.post("/", response_model=PersonNationalityResponse)
async def add_link(
    payload: PersonNationalityCreate,
    db: AsyncSession = Depends(get_db),
):
    new_link = PersonNationality(
        person_id=payload.person_id,
        country_id=payload.country_id,
    )
    db.add(new_link)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid person or country")

    await db.refresh(new_link)
    return new_link


# --------------------------------------------------------
# DELETE LINK
# --------------------------------------------------------
@router.delete("/{person_id}/{country_id}", status_code=204)
async def delete_link(
    person_id: str,
    country_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(PersonNationality).where(
            PersonNationality.person_id == person_id,
            PersonNationality.country_id == country_id,
        )
    )
    link = result.scalar_one_or_none()

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    await db.delete(link)
    await db.commit()
    return None
