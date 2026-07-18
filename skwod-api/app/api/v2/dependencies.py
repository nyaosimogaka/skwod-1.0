from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.security import decode_token
from app.models.users import User
from app.services.auth_service import user_has_permission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v2/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    payload = decode_token(token)

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401)

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=401)

    return user


def require_permission(action: str, resource: str):

    async def checker(
        user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):

        allowed = await user_has_permission(
            db,
            user.user_id,
            action,
            resource
        )

        if not allowed:
            raise HTTPException(status_code=403, detail="Forbidden")