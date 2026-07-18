from pydantic import BaseModel
from uuid import UUID


class PersonNationalityBase(BaseModel):
    person_id: UUID
    country_id: UUID


class PersonNationalityCreate(PersonNationalityBase):
    pass


class PersonNationalityResponse(PersonNationalityBase):
    model_config = {"from_attributes": True}
