from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BlogTeam(Base):
    """
    Link table: blog <-> team (many-to-many)
    """

    __tablename__ = "blog_team"

    blog_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blog.blog_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    team_id = Column(
        UUID(as_uuid=True),
        ForeignKey("team.team_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    # ----------------------------------------
    # RELATIONSHIPS
    # ----------------------------------------
    blog = relationship("Blog", back_populates="blog_team_links")
    team = relationship("Team", back_populates="blog_team_links")
    

    def __repr__(self):
        return f"<BlogTeam(team_id={self.team_id!r}, blog_id={self.blog_id!r})>"
