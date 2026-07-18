from sqlalchemy import Column, Text, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organization(Base):
    """
    SQLAlchemy model for the organization table.
    """

    __tablename__ = "organization"

    organization_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    organization_name = Column(
        Text(),
        nullable=False,
    )

    organization_type = Column(
        Text(),
        nullable=False,
    )

    # ----------------------
    # RELATIONSHIPS
    # ----------------------

    users = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    user_role = relationship("UserRoles", back_populates="organization")

    def __repr__(self):
        return (
            f"<Organization(organization_id={self.organization_id!r}, "
            f"organization_name={self.organization_name!r}, organization_type={self.organization_type!r})>"
        )
