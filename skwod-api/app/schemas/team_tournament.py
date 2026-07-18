# app/schemas/team_tournament.py
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class TeamTournamentBase(BaseModel):
    team_id: UUID
    tournament_id: UUID


class TeamTournamentCreate(TeamTournamentBase):
    pass


class TeamTournamentUpdate(BaseModel):
    team_id: UUID | None = None
    tournament_id: UUID | None = None


class TeamTournamentResponse(TeamTournamentBase):
    tt_id: UUID

    model_config = {"from_attributes": True}
