from fastapi import FastAPI, Body, Depends, File, UploadFile, Request
from fastapi.responses import FileResponse
from app.auth.jwt_bearer import jwtBearer
from app.auth.jwt_handler import *
from google.cloud import storage
from dotenv import load_dotenv
from app.encryptor import *
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
    mycursor = mydb.cursor()
    fullname = data.fullname
    email = data.email
    password = data.password
    password = password_encryption(password)
    hasPenis = data.hasPenis
    imgURL = data.PhotoURL
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
        query = "INSERT INTO User (Uid, Nama, Email, Password, hasPenis, Picture) VALUES (%s, %s, %s, %s, %s, %s);"
        res = (uid,fullname,email,password,hasPenis,imgURL)
        mycursor.execute(query, res)
        mydb.commit()
        mycursor.close()
        close_db_connection(mydb, "User")
        
        return True
    
def get_profile_user(email):
    mydb=defineDB()
    mycursor = mydb.cursor()
    res = (email,)
    mycursor.execute("SELECT * FROM User WHERE email= %s", res)
    myresult = mycursor.fetchall()
    mycursor.close()
    result_uid = myresult[0][0]
    result_email = myresult[0][1]
    result_nama = myresult[0][2]
    result_gender = myresult[0][4]
    result_picture = myresult[0][6]
    return {
        "uid":result_uid,
        "nama":result_nama,
        "email":result_email,
        "gender":result_gender,
        "photoURL":result_picture
    }



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
        res_pass = myresult[0][9]
        respassword = password_decryption(res_pass)
        if (password == respassword):
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
        resName = myresult[0][2]
        mycursor.close()
        close_db_connection(mydb, "User")
        return{
            "id" : resId,
            "Username" : resName
        }
    else:
        return{"error" : "what the hell are you trying to do 🗿"}
    

def get_tutor(specialization = None, category = None):
    mydb=defineDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Tutor ORDER BY id + 0 asc")
    myresult = mycursor.fetchall()
    tutors = []
    for x in myresult:
        tutor_items = {
            "id":x[0],
            "UserId":x[1],
            "Nama":x[2],
            "hasPenis":x[3],
            "AgesRanges":x[4],
            "Specialization":x[5],
            "Categories":x[6],
            "AboutMe":x[8],
            "SkillsAndExperiences":x[9],
            "picture":x[10],
            "price":x[11]
        }
        if specialization is not None and tutor_items["Specialization"].lower().find(specialization.lower()) != -1:
            if category is not None and tutor_items["Categories"] == category:
                tutors.append(tutor_items)
            elif category is None:
                tutors.append(tutor_items)

       
        elif specialization is None:
            if category is not None and tutor_items["Categories"] == category:
                tutors.append(tutor_items)
            elif category is None:
                tutors.append(tutor_items)



    mycursor.close()
    close_db_connection(mydb, "User")


    return tutors



def get_tutor_by_id(id_Tutor):
    mydb=defineDB()
    mycursor = mydb.cursor()
    res = (id_Tutor,)
    mycursor.execute("SELECT * FROM Tutor WHERE id = %s ORDER BY id + 0 asc", res)
    myresult = mycursor.fetchall()
    tutors = []
    for x in myresult:
        tutor_items = {
            "id":x[0],
            "UserId":x[1],
            "Nama":x[2],
            "hasPenis":x[3],
            "AgesRanges":x[4],
            "Specialization":x[5],
            "Categories":x[6],
            "AboutMe":x[8],
            "SkillsAndExperiences":x[9],
            "picture":x[10]
        }
        tutors.append(tutor_items) 
    mycursor.close()
    close_db_connection(mydb, "User")
    return tutors

def get_tutor_by_special(special):
    mydb=defineDB()
    mycursor = mydb.cursor()
    res = (special,)
    mycursor.execute("SELECT * FROM Tutor WHERE specialization = %s ORDER BY id + 0 asc", res)
    myresult = mycursor.fetchall()
    tutors = []
    for x in myresult:
        tutor_items = {
            "id":x[0],
            "UserId":x[1],
            "Nama":x[2],
            "hasPenis":x[3],
            "AgesRanges":x[4],
            "Specialization":x[5],
            "Categories":x[6],
            "AboutMe":x[8],
            "SkillsAndExperiences":x[9],
            "picture":x[10]
        }
        tutors.append(tutor_items) 
    mycursor.close()
    close_db_connection(mydb, "User")
    return tutors

def get_tutor_by_category(category):
    mydb=defineDB()
    mycursor = mydb.cursor()
    res = (category,)
    mycursor.execute("SELECT * FROM Tutor WHERE categories = %s ORDER BY id + 0 asc", res)
    myresult = mycursor.fetchall()
    tutors = []
    for x in myresult:
        tutor_items = {
            "id":x[0],
            "UserId":x[1],
            "Nama":x[2],
            "hasPenis":x[3],
            "AgesRanges":x[4],
            "Specialization":x[5],
            "Categories":x[6],
            "AboutMe":x[8],
            "SkillsAndExperiences":x[9],
            "picture":x[10]
        }
        tutors.append(tutor_items) 
    mycursor.close()
    close_db_connection(mydb, "User")
    return tutors