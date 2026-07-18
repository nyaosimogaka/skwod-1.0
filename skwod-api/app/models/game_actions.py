# app/models/game_actions.py
from sqlalchemy import (
    Column,
    Text,
    Float,
    ForeignKey,
    PrimaryKeyConstraint,
    Time,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base_class import Base


class GameActions(Base):
    """
    SQLAlchemy model for game_actions (composite PK).
    Primary key defined by: game_id, team_id, person_id, action_id, shot_clock
    """

    __tablename__ = "game_actions"

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
        ForeignKey("person.person_id", ondelete="SET NULL"),
        primary_key=True,
        nullable=False,
    )

    action_id = Column(
        UUID(as_uuid=True),
        ForeignKey("action.action_id", ondelete="RESTRICT"),
        primary_key=True,
        nullable=False,
    )

    shot_clock = Column(Time(), primary_key=True, nullable=False)  # part of PK

    action_timestamp = Column(DateTime(), nullable=True)
    outcome = Column(Text(), nullable=True)
    period = Column(Text(), nullable=True)
    timer = Column(Text(), nullable=True)

    x1 = Column(Float(), nullable=True)
    y1 = Column(Float(), nullable=True)
    x2 = Column(Float(), nullable=True)
    y2 = Column(Float(), nullable=True)

    # Relationships
    game = relationship("Game", back_populates="game_actions")
    team = relationship("Team", back_populates="game_actions")
    person = relationship("Person", back_populates="game_actions")
    action = relationship("Action", back_populates="game_actions")


    def __repr__(self) -> str:
        return (
            f"<GameActions(game_id={self.game_id!r}, team_id={self.team_id!r}, person_id={self.person_id!r}, "
            f"action_id={self.action_id!r}, shot_clock={self.shot_clock!r})>"
        )
