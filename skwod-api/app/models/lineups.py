# app/models/lineup.py
from sqlalchemy import Column, Text, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base


class Lineup(Base):
    """
    SQLAlchemy model for lineup (composite PK: game_id, team_id, person_id)
    Columns:
      - game_id   : uuid (FK -> game.game_id)
      - team_id   : uuid (FK -> team.team_id)
      - person_id : uuid (FK -> person.person_id)
      - role      : text, not null
      - is_captain: boolean, default False
    """

    __tablename__ = "lineup"

    game_id = Column(
        UUID(as_uuid=True),
        ForeignKey("game.game_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    team_id = Column(
        UUID(as_uuid=True),
        ForeignKey("team.team_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey("person.person_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    role = Column(Text(), nullable=False)
    is_captain = Column(Boolean(), nullable=True, default=False)

    # Relationships
    game = relationship("Game", back_populates="lineups")
    team = relationship("Team", back_populates="lineups")
    person = relationship("Person", back_populates="lineups")


    def __repr__(self) -> str:
        return f"<Lineup(game_id={self.game_id!r}, team_id={self.team_id!r}, person_id={self.person_id!r}, role={self.role!r})>"
