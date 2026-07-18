from sqlalchemy import Column, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Country(Base):
    """
    SQLAlchemy model for the country table.

    Columns:
      - country_id   : uuid, primary key
      - country_name : text, unique, not null
    """

    __tablename__ = "country"

    country_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    country_name = Column(
        Text(),
        nullable=False,
        unique=True,
    )

    # Relationships
    person_nationalities = relationship(
        "PersonNationality",
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    teams = relationship(
        "Team",
        back_populates="country",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<Country(country_id={self.country_id!r}, country_name={self.country_name!r})>"
