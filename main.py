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
        "request": request,
        "mode": None,
        "message": None,
        "alert": None
    })
    
@app.post("/auth", response_class=HTMLResponse)
async def auth_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(None),
    repeatedPassword: str = Form(None)
):
    if email == "test@gmail.com":
        message = "Enter your account."
        if password:
            return templates.TemplateResponse("index.html", {"request": request})  # Login success!
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "mode": "login",
            "message": message,
            "alert": None
        })
    else:
        message = "Create new account."
        alert = None
        if password and repeatedPassword:
            if password != repeatedPassword:
                alert = "Passwords don't match."
                return templates.TemplateResponse("auth.html", {
                    "request": request,
                    "mode": "register",
                    "alert": alert,
                    "message": message
                })
            return templates.TemplateResponse("index.html", {"request": request})
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "mode": "register",
            "alert": alert,
            "message": message
        })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)