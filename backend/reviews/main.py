from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/review/", response_class=HTMLResponse)
async def generate_review(request: Request):
    return templates.TemplateResponse("reviews/review.html", {"request": request})
