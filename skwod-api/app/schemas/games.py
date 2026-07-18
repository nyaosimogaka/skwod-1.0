# app/schemas/game.py
from typing import Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel


class GameBase(BaseModel):
    game_venue: str
    game_date: date
    tournament_id: UUID
    home_team: UUID
    away_team: UUID
    match_source: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    game_venue: Optional[str] = None
    game_date: Optional[date] = None
    tournament_id: Optional[UUID] = None
    home_team: Optional[UUID] = None
    away_team: Optional[UUID] = None
    match_source: Optional[str] = None


class GameResponse(GameBase):
    game_id: UUID

    model_config = {"from_attributes": True}
