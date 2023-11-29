from fastapi import FastAPI, Body, Depends, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi_pagination import Page, add_pagination, paginate, Params
from app.auth.jwt_bearer import jwtBearer
from app.auth.jwt_handler import *
from google.cloud import storage
from dotenv import load_dotenv
from app.model import *
from io import BytesIO
import mysql.connector
from app.function import *
from PIL import Image
import requests
import uvicorn
import random
import json
import jwt
import os
import io

 


users = []

posts = [
    {
        "id": 1,
        "title": "Thariq Fatturahman",
        "text":"Ineed more bullets hasta la vista baby, hasta la vista baby, Hello my name is jamal"

    },
    {
        "id": 2,
        "title": "Thariq Fatturahman2",
        "text": "Thariq Fatturahman2"

    },
    {
        "id": 3,
        "title":"Thariq Fatturahman3",
        "text":"Thariq Fatturahman3"

    }


]

app = FastAPI(
    title = "Tutoreal API",
    description = "Tutoreal backend api",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
    )
add_pagination(app)


@app.get("/decode/", dependencies=[Depends(jwtBearer())], tags=["decode"])
async def testcoded(request: Request):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    jsonResponse = decode_user(token2)
    return(jsonResponse["userID"])

def decode_user(token2):
    decoded_data = jwt.decode(token2,JWT_SECRET,JWT_ALGORITHM)
    return decoded_data




@app.get("/", tags=["welcome"])
def greet():
    return{
        "error":"false",
        "message":"Welcome to Tutoreal backend",
        "Features Status":[
            {

                "feature":"testing",
                "status":"true"

            },
            {

                "feature":"auth",
                "status":"false"
                
            }
        ]
    }

@app.get("/testing", tags=["testing"])
def testing():
    return posts



@app.post("/user/signup", tags=["user"])
async def user_signup(user : UserSchema = Body(...)):
    users.append(user)
    if push_user(user):
        return {
            "error":"false",
            "message":"User Created",
            "signupToken":signJWT(user.email)
            }
    else:
        raise HTTPException(status_code=409, detail="Bro the email already registered 💀")
    
@app.post("/user/signin", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        nanikore = signJWT(user.email)
        return {
            "error":"false",
            "message":"login success",
            "loginResult":{
            "userId":get_credentials(user),
            "token":nanikore,
            }}

    else:
        raise HTTPException(status_code=409, detail="Invalid login details bro 🗿")
    

@app.get("/tutor/alltutors", tags=["tutor"])
def get_all_tutors(specialization = None,category = None,params: Params = Depends()):
    tutors = get_tutor(specialization, category)
    if tutors:
        return {
            "error":"false",
            "message":"successfully fetching datas",
            "tutors":paginate(tutors, params=params)
        }
    else:
        return{
            "error":"false",
            "message":"successfully fetching datas",
            "tutors":{
                "item":[]
            }
        }
    
@app.get("/tutor/specialization", tags=["tutor"])
def get_tutor_by_specialization(specialization):
    tutors = get_tutor_by_special(specialization)
    if tutors:
        return {
            "error":"false",
            "message":"successfully fetching datas",
            "tutors":tutors
        }
    else:
        raise HTTPException(status_code=404, detail="Not Found sir 🗿")
    

@app.get("/tutor/category", tags=["tutor"])
def get_tutors_by_category(category):
    tutors = get_tutor_by_category(category)
    if tutors:
        return {
            "error":"false",
            "message":"successfully fetching datas",
            "tutors":tutors
        }
    else:
        raise HTTPException(status_code=404, detail="Not Found sir 🗿")

@app.get("/tutor/detail", tags=["tutor"])
def get_tutor_detail(tutor_id):
    tutor = get_tutor_by_id(tutor_id)
    if tutor:
        return {
            "error":"false",
            "message":"successfully fetching datas",
            "detail_tutor":tutor
        }
    else:
        raise HTTPException(status_code=404, detail="Not Found sir 🗿")
    

@app.get("/user/profile", dependencies=[Depends(jwtBearer())], tags=["profile"])
async def get_profile(request: Request):
    authHead = request.headers["Authorization"]
    authToken = authHead.split(" ")[1]
    jsonResponse = decode_user(authToken)
    if jsonResponse:
        return {
            "error":"false",
            "message":"successfully fetching user data",
            "user_data":get_profile_user(jsonResponse["userID"])
            }
    else:
        raise HTTPException(status_code=404, detail="User not Found sir 🗿")

@app.get("/user/history", dependencies=[Depends(jwtBearer())], tags=["history"])
async def get_history(request: Request):
    authHead = request.headers["Authorization"]
    authToken = authHead.split(" ")[1]
    jsonResponse = decode_user(authToken)
    if jsonResponse:
        return {
            "error":"false",
            "message":"successfully fetching user data",
            "user_data":get_profile_user(jsonResponse["userID"])
            }
    else:
        raise HTTPException(status_code=404, detail="User not Found sir 🗿")
    
@app.post("/user/new-history", dependencies=[Depends(jwtBearer())], tags=["history"])
async def post_history(request: Request, user : UserSchema = Body(...)):
    authHead = request.headers["Authorization"]
    authToken = authHead.split(" ")[1]
    jsonResponse = decode_user(authToken)
    if jsonResponse:
        return {
            "error":"false",
            "message":"successfully fetching user data",
            "user_data":get_profile_user(jsonResponse["userID"])
            }
    else:
        raise HTTPException(status_code=404, detail="User not Found sir 🗿")