from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.connection import get_db
from models.user import User

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    user_id = request.session.get('user_id')
    if not user_id:
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Not authenticated",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        return None
    user = await db.get(User, user_id)

    if not user:
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="User not found",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        return None
        
    return user
    