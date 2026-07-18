# app/schemas/person_team.py
from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel


class PersonTeamBase(BaseModel):
    team_id: UUID
    person_id: UUID
    person_type: str
    start_date: date | None = None
    end_date: date | None = None
    transfer_reason: str | None = None
    status: str | None = None
    pt_pic: str | None = None


class PersonTeamCreate(PersonTeamBase):
    pass


class PersonTeamUpdate(BaseModel):
    team_id: UUID | None = None
    person_id: UUID | None = None
    person_type: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    transfer_reason: str | None = None
    status: str | None = None
    pt_pic: str | None = None


class PersonTeamResponse(PersonTeamBase):
    pt_id: UUID

    model_config = {"from_attributes": True}
