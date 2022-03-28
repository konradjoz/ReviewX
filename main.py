from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models import User, Review, Shop, test
import datetime
from dotenv import *
from mongoengine import connect
import os
from pymongo import MongoClient
from dns import *
import json

app = FastAPI()
load_dotenv()
connect(host=os.getenv("MONGO_CONNECTION_STRING"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/index", response_class=RedirectResponse)
async def root(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})

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
            "update_time" : datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }

        return templates.TemplateResponse("error/user_not_found.html", context)
