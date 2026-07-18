# app/api/v1/games.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.games import Game
from app.schemas.games import GameCreate, GameResponse, GameUpdate

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=list[GameResponse])
async def list_games(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game))
    return result.scalars().all()


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game).where(Game.game_id == game_id))
    game = result.scalar_one_or_none()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/", response_model=GameResponse)
async def create_game(payload: GameCreate, db: AsyncSession = Depends(get_db)):
    new_game = Game(**payload.model_dump())
    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)
    return new_game


@router.put("/{game_id}", response_model=GameResponse)
async def update_game(game_id: str, payload: GameUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game).where(Game.game_id == game_id))
    game = result.scalar_one_or_none()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(game, field, value)

    await db.commit()
    await db.refresh(game)
    return game


@router.delete("/{game_id}", status_code=204)
async def delete_game(game_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game).where(Game.game_id == game_id))
    game = result.scalar_one_or_none()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    await db.delete(game)
    await db.commit()
    return None
