# app/models/game.py
from sqlalchemy import Column, Text, Date, ForeignKey, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base


class Game(Base):
    """
    SQLAlchemy model for the game table.

    Columns:
      - game_id       : uuid, not null, default uuid_generate_v4()
      - game_venue    : text, not null
      - game_date     : date, not null
      - tournament_id : uuid, not null (FK -> tournament.tournament_id)
      - home_team     : uuid, not null (FK -> team.team_id)
      - away_team     : uuid, not null (FK -> team.team_id)
      - match_source  : text, nullable
    """

    __tablename__ = "game"

    game_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
        doc="Primary key UUID (server-side generated)",
    )

    game_venue = Column(Text(), nullable=False)
    game_date = Column(Date(), nullable=False)

    tournament_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tournament.tournament_id", ondelete="CASCADE"),
        nullable=False,
    )

    home_team = Column(
        UUID(as_uuid=True),
        ForeignKey("team.team_id", ondelete="RESTRICT"),
        nullable=False,
    )

    away_team = Column(
        UUID(as_uuid=True),
        ForeignKey("team.team_id", ondelete="RESTRICT"),
        nullable=False,
    )

    match_source = Column(Text(), nullable=True)


    # Relationships
    tournament = relationship("Tournament", back_populates="games")

    home_team_rel = relationship(
        "Team",
        foreign_keys=[home_team],
        back_populates="home_games"
    )

    away_team_rel = relationship(
        "Team",
        foreign_keys=[away_team],
        back_populates="away_games"
    )

    lineups = relationship(
        "Lineup",
        back_populates="game",
        cascade="all, delete-orphan"
    )

    game_actions = relationship(
        "GameActions",
        back_populates="game",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Game(game_id={self.game_id!r}, game_date={self.game_date!r}, venue={self.game_venue!r})>"
