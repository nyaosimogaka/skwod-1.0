from sqlalchemy import Column, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.db.base_class import Base


class Resource(Base):
    """
    SQLAlchemy model for the resources table.
    """

    __tablename__ = "resources"

    resource_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    resource_name = Column(
        Text(),
        nullable=False,
    )

    # -------------
    # Relationships
    # -------------

    permission = relationship(
        "Permissions",
        back_populates="resource",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Resource(resource_id={self.resource_id!r}, "
            f"resource_name={self.resource_name!r})>"
        )
