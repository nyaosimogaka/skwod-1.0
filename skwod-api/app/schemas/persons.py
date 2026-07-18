from pydantic import BaseModel
from uuid import UUID
from datetime import date


class PersonBase(BaseModel):
    person_name: str
    person_dob: date | None = None
    person_pic: str | None = None
    person_height: float | None = None
    person_weight: float | None = None


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    person_name: str | None = None
    person_dob: date | None = None
    person_pic: str | None = None
    person_height: float | None = None
    person_weight: float | None = None


class PersonResponse(PersonBase):
    person_id: UUID

    model_config = {"from_attributes": True}
