from sqlalchemy import select
from app.models.users import User
from app.core.security import hash_password, verify_password


#Create User

async def create_user(db, payload):

    user = User(
        user_email=payload.email,
        user_password_hash=hash_password(payload.password),
        user_first_name=payload.first_name,
        user_last_name=payload.last_name,
        user_status="active"
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

#Authenticate User

async def authenticate_user(db, email, password):

    result = await db.execute(
        select(User).where(User.user_email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.user_password_hash):
        return None

    return user