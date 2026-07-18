from pydantic import BaseModel
from uuid import UUID


class CountryBase(BaseModel):
    country_name: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    country_name: str | None = None


class CountryResponse(CountryBase):
    country_id: UUID

    model_config = {"from_attributes": True}
