from sqlalchemy import Column, Text, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Tournament(Base):
    """
    SQLAlchemy model for the tournament table.
    """

    __tablename__ = "tournament"

    tournament_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    tournament_name = Column(
        Text(),
        nullable=False,
    )

    season = Column(Text(), nullable=True)

    subcategory = Column(Text(), nullable=True)

    parent_tournament_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tournament.tournament_id", ondelete="SET NULL"),
        nullable=True,
    )

    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sport.sport_id", ondelete="CASCADE"),
        nullable=False,
    )

    # -----------------------
    # RELATIONSHIPS
    # -----------------------

    sport = relationship("Sport", back_populates="tournaments")

    # Self-referencing parent tournament
    parent_tournament = relationship(
        "Tournament",
        remote_side=[tournament_id],
        back_populates="sub_tournaments",
    )

    # Children tournaments
    sub_tournaments = relationship(
        "Tournament",
        back_populates="parent_tournament",
        cascade="all, delete",
    )

    # many-to-many with Blog through BlogTournament
    blog_tournament_links = relationship(
        "BlogTournament",
        back_populates="tournament",
        cascade="all, delete-orphan"
    )

    # team_tournament (many-to-many: tournament ↔ team)
    team_tournaments = relationship(
        "TeamTournament",
        back_populates="tournament",
        cascade="all, delete-orphan"
    )

    # Games in this tournament
    games = relationship(
        "Game",
        back_populates="tournament",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Tournament(tournament_id={self.tournament_id!r}, "
            f"tournament_name={self.tournament_name!r})>"
        )
