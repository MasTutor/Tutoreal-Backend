from fastapi import FastAPI, Body, Depends, File, UploadFile, Request
from fastapi.responses import FileResponse
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
def user_signup(user : UserSchema = Body(...)):
    users.append(user)
    if push_user(user):
        return {
            "error":"false",
            "message":"User Created",
            "signupToken":signJWT(user.email)
            }
    else:
        return{
            "error":"true",
            "message":"Email already taken 🗿"
        }
    
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
        return{
            "error":"true",
            "message":"Invalid login details! 🗿"
        }