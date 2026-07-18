from pydantic import BaseModel
import uuid


class ActionBase(BaseModel):
    action_name: str
    short_name: str
    sport_id: uuid.UUID


class ActionCreate(ActionBase):
    pass


class ActionUpdate(BaseModel):
    action_name: str | None = None
    short_name: str | None = None
    sport_id: uuid.UUID | None = None


class ActionResponse(ActionBase):
    action_id: uuid.UUID

    class Config:
        from_attributes = True
