from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.blog_person import BlogPerson
from app.schemas.blog_person import (
    BlogPersonCreate,
    BlogPersonResponse,
)

router = APIRouter(prefix="/blog-person", tags=["blog-person"])


# --------------------------------------------------------
# LIST ALL BLOG-PERSON LINKS
# --------------------------------------------------------
@router.get("/", response_model=list[BlogPersonResponse])
async def list_links(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogPerson))
    links = result.scalars().all()
    return links


# --------------------------------------------------------
# CREATE LINK
# --------------------------------------------------------
@router.post("/", response_model=BlogPersonResponse)
async def add_link(
    payload: BlogPersonCreate,
    db: AsyncSession = Depends(get_db),
):
    new_link = BlogPerson(
        blog_id=payload.blog_id,
        person_id=payload.person_id,
    )
    db.add(new_link)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid blog or person")

    await db.refresh(new_link)
    return new_link


# --------------------------------------------------------
# DELETE LINK
# --------------------------------------------------------
@router.delete("/{blog_id}/{person_id}", status_code=204)
async def delete_link(
    blog_id: str,
    person_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(BlogPerson).where(
            BlogPerson.blog_id == blog_id,
            BlogPerson.person_id == person_id,
        )
    )
    link = result.scalar_one_or_none()

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    await db.delete(link)
    await db.commit()
    return None
