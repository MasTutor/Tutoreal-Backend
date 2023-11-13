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
from app.db import *
from PIL import Image
import requests
import uvicorn
import random
import uuid
import json
import jwt
import os
import io
import numpy as np


def push_user(data: UserSchema):
    uid = uuid.uuid4().hex
    mydb = defineDB()
    username = f"User_{uid}"
    mycursor = mydb.cursor()
    fullname = data.fullname
    email = data.email
    password = data.password
    hasPenis = data.hasPenis
    resq = (email,)

    mycursor.execute("SELECT * FROM User WHERE email= %s", resq)
    myresult = mycursor.fetchall()

    isTaken = "undefined"
    
    
    if (len(myresult) == 1):
        isTaken = True
    else:
        isTaken = False 

    if (isTaken):
        mycursor.close()
        close_db_connection(mydb, "User")
        
        return False
    else:
        query = "INSERT INTO User (Uid, Username, Nama, Email, Password, hasPenis) VALUES (%s, %s, %s, %s, %s, %s);"
        res = (uid,username,fullname,email,password,hasPenis)
        mycursor.execute(query, res)
        mydb.commit()
        mycursor.close()
        close_db_connection(mydb, "User")
        
        return True
    

def check_user(data: UserLoginSchema):
    mydb=defineDB()
    mycursor = mydb.cursor()

    email = data.email
    password = data.password
    res = (email,)

    mycursor.execute("SELECT * FROM User WHERE email= %s", res)
    myresult = mycursor.fetchall()
    mycursor.close()
    close_db_connection(mydb, "User")
    if (len(myresult) == 1):
        res_pass = myresult[0][3]
        if (password == res_pass):
            return True
    return False


def get_credentials(data: UserLoginSchema):
    mydb=defineDB()
    if check_user(data):
        mycursor = mydb.cursor()
        email = data.email
        res = (email,)
        mycursor.execute("SELECT * FROM User WHERE email= %s", res)
        myresult = mycursor.fetchall()
        resId = myresult[0][0]
        resName = myresult[0][1]
        mycursor.close()
        close_db_connection(mydb, "User")
        return{
            "id" : resId,
            "Username" : resName
        }
    else:
        return{"error" : "what the hell are you trying to do 🗿"}