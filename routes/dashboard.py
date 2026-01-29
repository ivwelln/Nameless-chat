from fastapi import APIRouter, Depends, HTTPException
from dependencies.connection import get_db
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Dashboard"])

templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request, db=Depends(get_db)):
    return templates.TemplateResponse("dashboard.html", {"request": request})