from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.countries import Country
from app.schemas.countries import CountryCreate, CountryUpdate, CountryResponse

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/", response_model=list[CountryResponse])
async def list_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country))
    return result.scalars().all()


@router.get("/{country_id}", response_model=CountryResponse)
async def get_country(country_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.country_id == country_id))
    country = result.scalar_one_or_none()
    if not country:
        raise HTTPException(404, "Country not found")
    return country


@router.post("/", response_model=CountryResponse)
async def add_country(payload: CountryCreate, db: AsyncSession = Depends(get_db)):
    new_country = Country(country_name=payload.country_name)
    db.add(new_country)
    await db.commit()
    await db.refresh(new_country)
    return new_country


@router.put("/{country_id}", response_model=CountryResponse)
async def update_country(country_id: str, payload: CountryUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.country_id == country_id))
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(404, "Country not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(country, field, value)

    await db.commit()
    await db.refresh(country)
    return country


@router.delete("/{country_id}", status_code=204)
async def delete_country(country_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Country).where(Country.country_id == country_id))
    country = result.scalar_one_or_none()

    if not country:
        raise HTTPException(404, "Country not found")

    await db.delete(country)
    await db.commit()
