from sqlalchemy import Column, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AuthActions(Base):
    """
    SQLAlchemy model for the auth_actions table.
    """

    __tablename__ = "auth_actions"

    auth_action_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    auth_action_name = Column(
        Text(),
        nullable=False,
    )

    # -------------
    # Relationships
    # -------------

    permission = relationship(
        "Permissions",
        back_populates="auth_action",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<AuthActions(auth_action_id={self.auth_action_id!r}, "
            f"auth_action_name={self.auth_action_name!r})>"
        )
