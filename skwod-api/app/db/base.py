from app.db.base_class import Base

# Existing models
from app.models.sports import Sport
from app.models.actions import Action
from app.models.countries import Country
from app.models.persons import Person
from app.models.teams import Team
from app.models.tournaments import Tournament
from app.models.person_nationality import PersonNationality
from app.models.blogs import Blog
from app.models.blog_person import BlogPerson
from app.models.blog_team import BlogTeam
from app.models.blog_tournament import BlogTournament
from app.models.team_tournament import TeamTournament
from app.models.person_team import PersonTeam
from app.models.person_participation import PersonParticipation
from app.models.games import Game
from app.models.lineups import Lineup
from app.models.game_actions import GameActions

# Auth models
from app.models.organizations import Organization
from app.models.users import User
from app.models.roles import Role
from app.models.permissions import Permissions
from app.models.resources import Resource
from app.models.auth_actions import AuthActions
from app.models.user_roles import UserRoles
from app.models.role_permissions import RolePermissions