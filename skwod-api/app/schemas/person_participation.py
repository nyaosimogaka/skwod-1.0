# app/schemas/person_participation.py
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class PersonParticipationBase(BaseModel):
    pt_id: UUID
    tt_id: UUID
    pp_pic: str | None = None


class PersonParticipationCreate(PersonParticipationBase):
    pass


class PersonParticipationUpdate(BaseModel):
    pt_id: UUID | None = None
    tt_id: UUID | None = None
    pp_pic: str | None = None


class PersonParticipationResponse(PersonParticipationBase):
    pp_id: UUID

    model_config = {"from_attributes": True}
