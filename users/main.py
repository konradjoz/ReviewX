from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from users.models import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/{username}", response_class=HTMLResponse)
async def user_profile(username: str, request: Request):
    if User.objects(username=username).count() == 1:
        users = User.objects.get(username=username)
        return templates.TemplateResponse("test.html", {"request": request, "users": users})
    else:
        raise HTTPException(status_code=404, detail="User not found")
        return
