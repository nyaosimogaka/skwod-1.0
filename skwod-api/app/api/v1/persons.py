from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.persons import Person
from app.schemas.persons import PersonCreate, PersonUpdate, PersonResponse

router = APIRouter(prefix="/persons", tags=["persons"])


# --------------------------------------------------------
# LIST PERSONS
# --------------------------------------------------------
@router.get("/", response_model=list[PersonResponse])
async def list_persons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Person))
    persons = result.scalars().all()
    return persons


# --------------------------------------------------------
# CREATE PERSON
# --------------------------------------------------------
@router.post("/", response_model=PersonResponse)
async def add_person(payload: PersonCreate, db: AsyncSession = Depends(get_db)):
    new_person = Person(
        person_name=payload.person_name,
        person_dob=payload.person_dob,
        person_pic=payload.person_pic,
        person_height=payload.person_height,
        person_weight=payload.person_weight,
    )

    db.add(new_person)
    await db.commit()
    await db.refresh(new_person)
    return new_person


# --------------------------------------------------------
# UPDATE PERSON
# --------------------------------------------------------
@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: str,
    payload: PersonUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Person).where(Person.person_id == person_id))
    person = result.scalar_one_or_none()

    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    # Apply only provided fields
    if payload.person_name is not None:
        person.person_name = payload.person_name

    if payload.person_dob is not None:
        person.person_dob = payload.person_dob

    if payload.person_pic is not None:
        person.person_pic = payload.person_pic

    if payload.person_height is not None:
        person.person_height = payload.person_height

    if payload.person_weight is not None:
        person.person_weight = payload.person_weight

    await db.commit()
    await db.refresh(person)
    return person


# --------------------------------------------------------
# DELETE PERSON
# --------------------------------------------------------
@router.delete("/{person_id}", status_code=204)
async def delete_person(person_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Person).where(Person.person_id == person_id))
    person = result.scalar_one_or_none()

    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")

    await db.delete(person)
    await db.commit()
    return None
