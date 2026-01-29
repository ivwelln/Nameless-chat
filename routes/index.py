from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies.connection import get_db
from dependencies.auth import get_current_user
from dependencies.chat import get_chats_for_current_user
from models.user import User
from models.chat import Chat

router = APIRouter(tags=["MainPage"])

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    user = None

    user = await get_current_user(request, db)
    # print(user.username if user else "No user")
    chats = await get_chats_for_current_user(request, db)

    return templates.TemplateResponse("index.html", {"request": request, "user": user, "chats": chats})