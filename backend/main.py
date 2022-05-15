import datetime
import os as os

from dotenv import *
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mongoengine import connect
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.main import router as api_router
from config import settings
from models import *
from reviews.main import router as review_router
from users.main import router as user_router
from users.models import User

app = FastAPI()

# CORS middleware for cross-origin requests (development)
# Allows the connection between the frontend (React) and the backend (FastAPI)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# COnnecting to MongoDB database
dotenv_path_variable = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path_variable)
db = connect(host=os.getenv("MONGO_URI"))

# Mounting the static files directory to the app (for CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/javascript", StaticFiles(directory="javascript"), name="javascript")

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

app.include_router(api_router, prefix="/api/v1")
app.include_router(user_router, prefix="/users")
app.include_router(review_router, prefix="/reviews")


@app.on_event("startup")
async def startup():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()


# Index Route
@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/login/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/verify", response_class=HTMLResponse)
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if User.objects(username=username).count() == 1:
        users = User.objects.get(username=username)
        if users.password == password:
            {"request": request, "users": users}
            return RedirectResponse(url=f'/users/{username}')
        else:
            context = {
                "request": request,
                "login_status": True,
                "update_time": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
            return templates.TemplateResponse("login.html", context)
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/merchants", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("merchants/merchants.html", {"request": request})


@app.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    merchants_list = []
    for merchant in Shop.objects().fields(name=1):
        merchants_list.append(merchant.name)
    return templates.TemplateResponse("terms.html", {"request": request})


@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})


# Default Exception Route
@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exc: StarletteHTTPException):
    # print(exc.status_code, exc.detail)
    error_status = exc.status_code
    if exc.status_code == 404:
        return templates.TemplateResponse('error/error.html', {
            'request': request,
            'error_status': error_status,
            'detail': exc.detail
        })
    elif exc.status_code == 500:
        return templates.TemplateResponse('error/error.html', {
            'request': request,
            'error_status': error_status,
            'detail': exc.detail
        })
    else:
        # Generic error page
        return templates.TemplateResponse('error/error.html', {
            'request': request,
            'error_status': error_status,
            'detail': exc.detail
        })
