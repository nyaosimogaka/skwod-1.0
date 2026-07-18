from pydantic import BaseModel
from uuid import UUID


class TeamBase(BaseModel):
    team_name: str
    team_type: str
    nickname: str | None = None
    team_logo: str | None = None
    sport_id: UUID
    country_id: UUID


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    team_name: str | None = None
    team_type: str | None = None
    nickname: str | None = None
    team_logo: str | None = None
    sport_id: UUID | None = None
    country_id: UUID | None = None


class TeamResponse(TeamBase):
    team_id: UUID

    model_config = {"from_attributes": True}

