# app/schemas/lineup.py
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class LineupBase(BaseModel):
    game_id: UUID
    team_id: UUID
    person_id: UUID
    role: str
    is_captain: Optional[bool] = False


class LineupCreate(LineupBase):
    pass


class LineupUpdate(BaseModel):
    role: Optional[str] = None
    is_captain: Optional[bool] = None


class LineupResponse(LineupBase):
    # composite PK returned in response as fields
    model_config = {"from_attributes": True}
