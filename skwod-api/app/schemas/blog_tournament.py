from pydantic import BaseModel
from uuid import UUID


class BlogTournamentBase(BaseModel):
    blog_id: UUID
    tournament_id: UUID


class BlogTournamentCreate(BlogTournamentBase):
    pass


class BlogTournamentResponse(BlogTournamentBase):
    model_config = {"from_attributes": True}
