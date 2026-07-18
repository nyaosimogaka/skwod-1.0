from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# Shared fields for reading from DB OR creating new sports
class SportBase(BaseModel):
    sport_name: str


# Schema for creating a new sport
class SportCreate(SportBase):
    pass


# Schema for reading/returning a sport from DB
class SportResponse(SportBase):
    sport_id: UUID

    model_config = {
        "from_attributes": True  # Allows ORM model -> Pydantic conversion
    }