# app/schemas/game_actions.py
from typing import Optional
from uuid import UUID
from datetime import datetime, time
from pydantic import BaseModel


class GameActionsBase(BaseModel):
    game_id: UUID
    team_id: UUID
    person_id: UUID
    action_id: UUID
    shot_clock: time

    action_timestamp: Optional[datetime] = None
    outcome: Optional[str] = None
    period: Optional[str] = None
    timer: Optional[str] = None

    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    y2: Optional[float] = None


class GameActionsCreate(GameActionsBase):
    pass


class GameActionsUpdate(BaseModel):
    action_timestamp: Optional[datetime] = None
    outcome: Optional[str] = None
    period: Optional[str] = None
    timer: Optional[str] = None
    x1: Optional[float] = None
    y1: Optional[float] = None
    x2: Optional[float] = None
    y2: Optional[float] = None


class GameActionsResponse(GameActionsBase):
    model_config = {"from_attributes": True}
