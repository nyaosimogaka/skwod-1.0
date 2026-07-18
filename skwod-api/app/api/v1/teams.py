from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.teams import Team
from app.schemas.teams import TeamCreate, TeamUpdate, TeamResponse

router = APIRouter(prefix="/teams", tags=["teams"])


# --------------------------------------------------------
# LIST TEAMS
# --------------------------------------------------------
@router.get("/", response_model=list[TeamResponse])
async def list_teams(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Team))
    teams = result.scalars().all()
    return teams


# --------------------------------------------------------
# CREATE TEAM
# --------------------------------------------------------
@router.post("/", response_model=TeamResponse)
async def add_team(payload: TeamCreate, db: AsyncSession = Depends(get_db)):
    new_team = Team(
        team_name=payload.team_name,
        team_type=payload.team_type,
        nickname=payload.nickname,
        team_logo=payload.team_logo,
        sport_id=payload.sport_id,
        country_id=payload.country_id,
    )

    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)
    return new_team


# --------------------------------------------------------
# UPDATE TEAM
# --------------------------------------------------------
@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: str,
    payload: TeamUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Team).where(Team.team_id == team_id))
    team = result.scalar_one_or_none()

    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    # Apply only provided fields
    if payload.team_name is not None:
        team.team_name = payload.team_name

    if payload.team_type is not None:
        team.team_type = payload.team_type

    if payload.nickname is not None:
        team.nickname = payload.nickname

    if payload.team_logo is not None:
        team.team_logo = payload.team_logo

    if payload.sport_id is not None:
        team.sport_id = payload.sport_id

    if payload.country_id is not None:
        team.country_id = payload.country_id

    await db.commit()
    await db.refresh(team)
    return team


# --------------------------------------------------------
# DELETE TEAM
# --------------------------------------------------------
@router.delete("/{team_id}", status_code=204)
async def delete_team(
    team_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Team).where(Team.team_id == team_id))
    team = result.scalar_one_or_none()

    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    await db.delete(team)
    await db.commit()
    return None
