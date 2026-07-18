from sqlalchemy import Column, Text, text, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Team(Base):
    """
    SQLAlchemy model for the team table.
    """

    __tablename__ = "team"

    team_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=text("uuid_generate_v4()"),
    )

    team_name = Column(Text(), nullable=False)
    team_type = Column(Text(), nullable=False)
    nickname = Column(Text(), nullable=True)
    team_logo = Column(Text(), nullable=True)

    sport_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sport.sport_id", ondelete="CASCADE"),
        nullable=False,
    )

    country_id = Column(
        UUID(as_uuid=True),
        ForeignKey("country.country_id", ondelete="RESTRICT"),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("team_type IN ('NT', 'CLUB')", name="team_team_type_check"),
    )

    # Relationships
    sport = relationship("Sport", back_populates="teams")
    country = relationship("Country", back_populates="teams")

    # many-to-many with Blog through BlogTeam
    blog_team_links = relationship(
        "BlogTeam",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    # team_tournament (many-to-many: team ↔ tournament)
    team_tournaments = relationship(
        "TeamTournament",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    # person_team (players/coaches assigned to a team)
    person_teams = relationship(
        "PersonTeam",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    # Game relationships
    home_games = relationship(
        "Game",
        foreign_keys="Game.home_team",
        back_populates="home_team_rel"
    )

    away_games = relationship(
        "Game",
        foreign_keys="Game.away_team",
        back_populates="away_team_rel"
    )

    lineups = relationship(
        "Lineup",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    game_actions = relationship(
        "GameActions",
        back_populates="team",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Team(team_id={self.team_id!r}, team_name={self.team_name!r})>"
