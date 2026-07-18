from sqlalchemy import Column, Text, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Blog(Base):
    """
    SQLAlchemy model for the blog table.
    """

    __tablename__ = "blog"

    blog_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    title = Column(
        Text(),
        nullable=False,
    )

    author = Column(
        Text(),
        nullable=False,
    )

    slug = Column(
        Text(),
        nullable=False,
    )

    content = Column(
        Text(),
        nullable=False,
    )

    # ----------------------------------------
    # RELATIONSHIPS
    # ----------------------------------------

    # Link table relationship
    blog_person_links = relationship(
        "BlogPerson",
        back_populates="blog",
        cascade="all, delete-orphan"
    )

    blog_team_links = relationship(
        "BlogTeam",
        back_populates="blog",
        cascade="all, delete-orphan"
    )

    blog_tournament_links = relationship(
        "BlogTournament",
        back_populates="blog",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Blog(blog_id={self.blog_id!r}, "
            f"title={self.title!r}, author={self.author!r}, slug={self.slug!r}, content={self.content!r})>"
        )
