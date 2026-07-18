from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.blogs import Blog
from app.schemas.blogs import BlogCreate, BlogUpdate, BlogResponse

router = APIRouter(prefix="/blogs", tags=["blogs"])


# ------------------------
# GET all actions
# ------------------------
@router.get("/", response_model=list[BlogResponse])
async def list_blogs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog))
    return result.scalars().all()


# ------------------------
# GET blog by ID
# ------------------------
@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.blog_id == blog_id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    return blog


# ------------------------
# CREATE new blog
# ------------------------
@router.post("/", response_model=BlogResponse)
async def create_blog(payload: BlogCreate, db: AsyncSession = Depends(get_db)):
    new_blog = Blog(
        title=payload.title,
        author=payload.author,
        slug=payload.slug,
        content=payload.content
    )

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)

    return new_blog


# ------------------------
# UPDATE existing blog
# ------------------------
@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: str,
    payload: BlogUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Blog).where(Blog.blog_id == blog_id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # partial update
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(blog, key, value)

    await db.commit()
    await db.refresh(blog)

    return blog


# ------------------------
# DELETE blog
# ------------------------
@router.delete("/{blog_id}")
async def delete_blog(blog_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.blog_id == blog_id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    await db.delete(blog)
    await db.commit()

    return {"message": "Blog deleted successfully"}
