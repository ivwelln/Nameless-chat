from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from contextlib import asynccontextmanager

from models import User
from database import engine, Base, get_async_session
from auth_utils import hash_password, verify_password, create_access_token, decode_access_token

MAX_FAILED_ATTEMPTS = 5
LOCK_MINUTES = 15
COOKIE_NAME = "access_token"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Таблицы успешно созданы")
    yield
    await engine.dispose()
    print("🛑 Подключение к БД закрыто")
    
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
        
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def auth_get(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})
    
@app.post("/auth/check-email")
async def check_email(email: str = Form(...), session=Depends(get_async_session)):
    if (email.lower() == "test@gmail.com"):
        return {"mode" : "login", "message" : "Enter your account."}
    else:
        return {"mode" : "register", "message" : "Create new account."}

@app.post("/auth/submit")
async def sumbit(
    email: str = Form(...),
    password: str = Form(...),
    repeatedPassword: str = Form(None)
):
    if (email == "test@gmail.com"):
        if (password == "123"):
            return {"success" : True, "redirect" : "/"}
        else:
            return {"success" : False, "alert" : "Wrong password."}
    else: 
        if (password != repeatedPassword):
            return {"success": False, "alert" : "Passwords don't match."}
        else: 
            return {"success": True, "redirect" : "/"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)