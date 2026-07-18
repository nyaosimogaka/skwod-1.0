from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class PersonNationality(Base):
    """
    Link table: person <-> country (many-to-many)
    """

    __tablename__ = "person_nationality"

    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey("person.person_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    country_id = Column(
        UUID(as_uuid=True),
        ForeignKey("country.country_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    # Relationships
    person = relationship("Person", back_populates="nationalities")
    country = relationship("Country", back_populates="person_nationalities")

    def __repr__(self):
        return f"<PersonNationality(person_id={self.person_id!r}, country_id={self.country_id!r})>"
