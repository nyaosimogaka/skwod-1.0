from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.blog_tournament import BlogTournament
from app.schemas.blog_tournament import (
    BlogTournamentCreate,
    BlogTournamentResponse,
)

router = APIRouter(prefix="/blog-tournament", tags=["blog-tournament"])


# --------------------------------------------------------
# LIST ALL BLOG-TOURNAMENT LINKS
# --------------------------------------------------------
@router.get("/", response_model=list[BlogTournamentResponse])
async def list_links(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogTournament))
    links = result.scalars().all()
    return links


# --------------------------------------------------------
# CREATE LINK
# --------------------------------------------------------
@router.post("/", response_model=BlogTournamentResponse)
async def add_link(
    payload: BlogTournamentCreate,
    db: AsyncSession = Depends(get_db),
):
    new_link = BlogTournament(
        blog_id=payload.blog_id,
        tournament_id=payload.tournament_id,
    )
    db.add(new_link)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid blog or tournament")

    await db.refresh(new_link)
    return new_link


# --------------------------------------------------------
# DELETE LINK
# --------------------------------------------------------
@router.delete("/{blog_id}/{tournament_id}", status_code=204)
async def delete_link(
    blog_id: str,
    tournament_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(BlogTournament).where(
            BlogTournament.blog_id == blog_id,
            BlogTournament.tournament_id == tournament_id,
        )
    )
    link = result.scalar_one_or_none()

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    await db.delete(link)
    await db.commit()
    return None
