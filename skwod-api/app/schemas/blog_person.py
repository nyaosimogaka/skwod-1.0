from pydantic import BaseModel
from uuid import UUID


class BlogPersonBase(BaseModel):
    blog_id: UUID
    person_id: UUID


class BlogPersonCreate(BlogPersonBase):
    pass


class BlogPersonResponse(BlogPersonBase):
    model_config = {"from_attributes": True}
