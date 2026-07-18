from pydantic import BaseModel
from uuid import UUID


class BlogTeamBase(BaseModel):
    blog_id: UUID
    team_id: UUID


class BlogTeamCreate(BlogTeamBase):
    pass


class BlogTeamResponse(BlogTeamBase):
    model_config = {"from_attributes": True}
