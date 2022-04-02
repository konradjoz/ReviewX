import datetime

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from user.models import User

router = APIRouter(prefix='/user')


@router.get("/{username}", response_class=HTMLResponse)
async def user_profile(username: str, request: Request):
    if User.objects(username=username).count() == 1:
        users = User.objects.get(username=username)
        return templates.TemplateResponse("test.html", {"request": request, "user": users})
    else:
        context = {
            "request": request,
            "username": username,
            "update_time": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }
        return templates.TemplateResponse("error/user_not_found.html", context)
