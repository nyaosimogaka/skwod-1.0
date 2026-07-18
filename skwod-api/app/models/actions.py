from sqlalchemy import Column, Text, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Action(Base):
    """
    SQLAlchemy model for the action table.
    """

    __tablename__ = "action"

    action_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    action_name = Column(
        Text(),
        nullable=False,
    )

    short_name = Column(
        Text(),
        nullable=False,
    )

    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sport.sport_id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationship back to sport
    sport = relationship("Sport", back_populates="actions")

    # Relationship back to game_actions
    game_actions = relationship(
        "GameActions",
        back_populates="action",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Action(action_id={self.action_id!r}, "
            f"action_name={self.action_name!r}, short_name={self.short_name!r})>"
        )
