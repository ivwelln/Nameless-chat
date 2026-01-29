from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from core.database import engine
from models.base import Base

from models.chat import Chat
from models.user import User
from models.message import Message
from models.chat_member import ChatMember

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key="to_change_that_later") # TODO: Change secret key.

from routes import auth
from routes import index
from routes import dashboard
from routes import chat

app.include_router(auth.router)
app.include_router(index.router)
app.include_router(dashboard.router)
app.include_router(chat.router)