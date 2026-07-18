from sqlalchemy import Column, Text, text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Role(Base):
    """
    SQLAlchemy model for the role table.
    """

    __tablename__ = "roles"

    role_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    role_name = Column(
        Text(),
        nullable=False,
    )

    # -------------
    # Relationships
    # -------------
    
    role_permission = relationship("RolePermissions", back_populates="role")
    user_role = relationship("UserRoles", back_populates="role")

    def __repr__(self):
        return (
            f"<Role(role_id={self.role_id!r}, "
            f"role_name={self.role_name!r})>"
        )
