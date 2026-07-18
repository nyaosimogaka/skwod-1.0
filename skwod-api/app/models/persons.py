from sqlalchemy import Column, Text, Date, Float, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Person(Base):
    """
    SQLAlchemy model for the person table.
    """

    __tablename__ = "person"

    person_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    person_name = Column(Text(), nullable=False)
    person_dob = Column(Date(), nullable=True)
    person_pic = Column(Text(), nullable=True)
    person_height = Column(Float(), nullable=True)
    person_weight = Column(Float(), nullable=True)

    # Relationships
    nationalities = relationship(
        "PersonNationality",
        back_populates="person",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # many-to-many with Blog through BlogPerson
    blog_person_links = relationship(
        "BlogPerson",
        back_populates="person",
        cascade="all, delete-orphan"
    )

    # person_team (links person <-> team)
    person_teams = relationship(
        "PersonTeam",
        back_populates="person",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # person_participation (player/coach participation in team_tournament)
    person_participations = relationship(
        "PersonParticipation",
        secondary="person_team",
        primaryjoin="Person.person_id==PersonTeam.person_id",
        secondaryjoin="PersonTeam.pt_id==PersonParticipation.pt_id",
        viewonly=True
    )

    # Lineups the person appears in
    lineups = relationship(
        "Lineup",
        back_populates="person",
        cascade="all, delete-orphan"
    )

    game_actions = relationship(
        "GameActions",
        back_populates="person",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Person(person_id={self.person_id!r}, person_name={self.person_name!r})>"
