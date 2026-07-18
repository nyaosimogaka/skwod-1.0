from sqlalchemy import Column, Text, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """
    SQLAlchemy model for the users table.
    """

    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organization.organization_id", ondelete="CASCADE"),
        nullable=False,
    )

    user_email = Column(
        Text(),
        nullable=False,
    )

    user_password_hash = Column(
        Text(),
        nullable=False,
    )

    user_first_name = Column(
        Text(),
        nullable=False,
    )

    user_last_name = Column(
        Text(),
        nullable=False,
    )

    user_status = Column(
        Text(),
        nullable=False,
    )

    # ----------------------
    # RELATIONSHIPS
    # ----------------------
    
    organization = relationship("Organization", back_populates="users")
    user_role = relationship("UserRoles", back_populates="users")

    def __repr__(self):
        return (
            f"<Organization(organization_id={self.organization_id!r}, "
            f"organization_name={self.organization_name!r}, organization_type={self.organization_type!r})>"
        )
