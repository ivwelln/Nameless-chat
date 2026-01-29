from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from schemas.user import UserCreate, UserRead
from schemas.auth import LoginRequest
from dependencies.connection import get_db
from core.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

templates = Jinja2Templates(directory="templates")

@router.get("", response_class=HTMLResponse)
async def read_auth(request: Request):
    # Если пользователь уже авторизирован, то зачем ему снова видеть форму с авторизацией???
    if request.session.get("user_id"):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("auth.html", {"request": request})

@router.post("/register", response_model=UserRead)
async def register_user(
    user: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Проверка существования
    result = await db.execute(
        select(User).where((User.email == user.email) | (User.username == user.username))
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    if user.password != user.repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    password_hash = hash_password(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password_hash=password_hash
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Логин после регистрации
    request.session["user_id"] = db_user.id

    return db_user

@router.post("/login")
async def login_user(data: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Проверка пароля
    if not verify_password(data.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    request.session['user_id'] = db_user.id
    
    return RedirectResponse(url="/", status_code=303)

@router.post("/logout")
async def logout_user(request: Request):
    print(request.session)
    request.session.clear()
    print(request.session)
    return RedirectResponse(url="/auth", status_code=303)