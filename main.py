from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def auth_get(request: Request):
    return templates.TemplateResponse("auth.html", {
        "request": request
    })
    
@app.post("/auth/check-email")
async def check_email(email: str = Form(...)):
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