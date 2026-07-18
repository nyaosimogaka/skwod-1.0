from pydantic import BaseModel
import uuid


class BlogBase(BaseModel):
    title: str
    author: str
    slug: str
    content: str


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    slug: str | None = None
    content: str | None = None


class BlogResponse(BlogBase):
    blog_id: uuid.UUID

    class Config:
        from_attributes = True
