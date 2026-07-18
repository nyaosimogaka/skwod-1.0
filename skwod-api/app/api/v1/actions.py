from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.actions import Action
from app.schemas.actions import ActionCreate, ActionUpdate, ActionResponse

router = APIRouter(prefix="/actions", tags=["actions"])


# ------------------------
# GET all actions
# ------------------------
@router.get("/", response_model=list[ActionResponse])
async def list_actions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Action))
    return result.scalars().all()


# ------------------------
# GET action by ID
# ------------------------
@router.get("/{action_id}", response_model=ActionResponse)
async def get_action(action_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Action).where(Action.action_id == action_id))
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    return action


# ------------------------
# CREATE new action
# ------------------------
@router.post("/", response_model=ActionResponse)
async def create_action(payload: ActionCreate, db: AsyncSession = Depends(get_db)):
    new_action = Action(
        action_name=payload.action_name,
        short_name=payload.short_name,
        sport_id=payload.sport_id,
    )

    db.add(new_action)
    await db.commit()
    await db.refresh(new_action)

    return new_action


# ------------------------
# UPDATE existing action
# ------------------------
@router.put("/{action_id}", response_model=ActionResponse)
async def update_action(
    action_id: str,
    payload: ActionUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Action).where(Action.action_id == action_id))
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    # partial update
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(action, key, value)

    await db.commit()
    await db.refresh(action)

    return action


# ------------------------
# DELETE action
# ------------------------
@router.delete("/{action_id}")
async def delete_action(action_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Action).where(Action.action_id == action_id))
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(status_code=404, detail="Action not found")

    await db.delete(action)
    await db.commit()

    return {"message": "Action deleted successfully"}
