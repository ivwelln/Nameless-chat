from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.connection import get_db
from sqlalchemy.future import select
from models.chat import Chat
from models.chat_member import ChatMember
from models.user import User
from dependencies.chat import create_chat_for_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/create")
async def create_chat(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    await create_chat_for_current_user(request, db)
    