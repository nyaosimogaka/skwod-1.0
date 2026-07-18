from pydantic import BaseModel
import uuid


class TournamentBase(BaseModel):
    tournament_name: str
    season: str | None = None
    subcategory: str | None = None
    parent_tournament_id: uuid.UUID | None = None
    sport_id: uuid.UUID


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(BaseModel):
    tournament_name: str | None = None
    season: str | None = None
    subcategory: str | None = None
    parent_tournament_id: uuid.UUID | None = None
    sport_id: uuid.UUID | None = None


class TournamentResponse(TournamentBase):
    tournament_id: uuid.UUID

    class Config:
        from_attributes = True
