from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BlogTournament(Base):
    """
    Link table: blog <-> tournament (many-to-many)
    """

    __tablename__ = "blog_tournament"

    blog_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blog.blog_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    tournament_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tournament.tournament_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    # ----------------------------------------
    # RELATIONSHIPS
    # ----------------------------------------
    blog = relationship("Blog", back_populates="blog_tournament_links")
    tournament = relationship("Tournament", back_populates="blog_tournament_links")
    

    def __repr__(self):
        return f"<BlogTournament(tournament_id={self.tournament_id!r}, blog_id={self.blog_id!r})>"
