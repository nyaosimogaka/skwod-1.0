from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.blog_team import BlogTeam
from app.schemas.blog_team import (
    BlogTeamCreate,
    BlogTeamResponse,
)

router = APIRouter(prefix="/blog-team", tags=["blog-team"])


# --------------------------------------------------------
# LIST ALL BLOG-TEAM LINKS
# --------------------------------------------------------
@router.get("/", response_model=list[BlogTeamResponse])
async def list_links(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogTeam))
    links = result.scalars().all()
    return links


# --------------------------------------------------------
# CREATE LINK
# --------------------------------------------------------
@router.post("/", response_model=BlogTeamResponse)
async def add_link(
    payload: BlogTeamCreate,
    db: AsyncSession = Depends(get_db),
):
    new_link = BlogTeam(
        blog_id=payload.blog_id,
        team_id=payload.team_id,
    )
    db.add(new_link)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid blog or team")

    await db.refresh(new_link)
    return new_link


# --------------------------------------------------------
# DELETE LINK
# --------------------------------------------------------
@router.delete("/{blog_id}/{team_id}", status_code=204)
async def delete_link(
    blog_id: str,
    team_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(BlogTeam).where(
            BlogTeam.blog_id == blog_id,
            BlogTeam.team_id == team_id,
        )
    )
    link = result.scalar_one_or_none()

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    await db.delete(link)
    await db.commit()
    return None
