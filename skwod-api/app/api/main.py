"""
Entrypoint for the FastAPI application.
"""
from fastapi import FastAPI
from app.core.settings import settings
from app.api.v1.sports import router as sports_router
from app.api.v1.actions import router as actions_router
from app.api.v1.tournaments import router as tournaments_router
from app.api.v1.countries import router as countries_router
from app.api.v1.persons import router as persons_router
from app.api.v1.teams import router as teams_router
from app.api.v1.person_nationality import router as person_nationality_router
from app.api.v1.blogs import router as blogs_router
from app.api.v1.blog_person import router as blog_person_router
from app.api.v1.blog_team import router as blog_team_router
from app.api.v1.blog_tournament import router as blog_tournament_router
from app.api.v1.team_tournament import router as team_tournament_router
from app.api.v1.person_team import router as person_team_router
from app.api.v1.person_participation import router as person_participation_router
from app.api.v1.games import router as games_router
from app.api.v1.lineups import router as lineups_router
from app.api.v1.game_actions import router as game_actions_router
from app.api.v2 import auth as auth_v2

app = FastAPI(title="skwod-api")

# register routers here
app.include_router(sports_router)
app.include_router(countries_router)
app.include_router(actions_router)
app.include_router(tournaments_router)
app.include_router(teams_router)
app.include_router(persons_router)
app.include_router(person_nationality_router)
app.include_router(blogs_router)
app.include_router(blog_person_router)
app.include_router(blog_team_router)
app.include_router(blog_tournament_router)
app.include_router(team_tournament_router)
app.include_router(person_team_router)
app.include_router(person_participation_router)
app.include_router(games_router)
app.include_router(lineups_router)
app.include_router(game_actions_router)
app.include_router(auth_v2.router, prefix="/v2")

@app.get("/")
def root():
    return {"message": "Hello from skwod-api!", "env": settings.ENV}
