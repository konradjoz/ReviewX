import datetime
import os as os

from dotenv import *
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mongoengine import connect
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from models import User, Shop

app = FastAPI()

date_now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

dotenv_path_variable = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path_variable)
connect(host=os.getenv("MONGO_URI"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get("/login/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/", response_class=HTMLResponse)
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if User.objects(username=username).count() == 1:
        users = User.objects.get(username=username)
        if users.password == password:
            context = {"request": request, "user": users}
            return RedirectResponse(url=f'/user/{username}')
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


@app.get("/user/{username}", response_class=HTMLResponse)
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


@app.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})


@app.get("/api/v1/merchants", response_class=JSONResponse)
async def get_merchants():
    merchants_list = {
        "merchants": []
    }
    for merchant in Shop.objects().fields(name=1):
        merchants_list["merchants"].append(merchant.name)
    if len(merchants_list["merchants"]) != 0:
        return JSONResponse(merchants_list)
    else:
        return JSONResponse({
            "message": "No merchants found"
        })


@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
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
