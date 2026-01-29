from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from dependencies.connection import get_db
from models.user import User
from models.chat import Chat
from models.chat_member import ChatMember
from typing import List

async def get_chats_for_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> List[Chat]:
    user_id = request.session.get('user_id')
    if not user_id:
        return []
    
    result = await db.execute(
        select(Chat).join(ChatMember).where(ChatMember.user_id == user_id)
    )
    chats = result.scalars().all()

    return chats

async def create_chat_for_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> Chat:
    user_id = request.session.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    new_chat = Chat(name = "Новый чат", owner_id=user_id)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    
    chat_member = ChatMember(chat_id=new_chat.id, user_id=user_id)
    db.add(chat_member)
    await db.commit()
    
    print(f"Created new chat with ID: {new_chat.id} for user ID: {user_id} with {new_chat.name} name")
    
    return new_chat
