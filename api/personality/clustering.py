import requests
import numpy as np
from decouple import config
from dotenv import load_dotenv
import os
import ast
from fastapi import FastAPI, Body, Depends, File, UploadFile, Request
from fastapi.responses import FileResponse
from api.auth.jwt_bearer import jwtBearer
from api.auth.jwt_handler import *
from google.cloud import storage
from dotenv import load_dotenv
from api.encryptor import *
from api.model import *
from io import BytesIO
import mysql.connector
from api.function import *
from api.db import *
from PIL import Image
import requests
import os
import numpy as np


def post_answer(data, email):
    try:
        _data = ast.literal_eval(data)
        if(len(_data) != 25):
            return {"error":"true",
                    "message":"Please Input 25 length list"}
        mydb = defineDB()
        mycursor = mydb.cursor()
        sql = "UPDATE User SET answer = %s WHERE Email = %s"
        mycursor.execute(sql, (data, email))
        mydb.commit()
        mycursor.close()
        close_db_connection(mydb, "User")
        process_user_data()
        return {"error":"false",
                "message":"successfully added the personality"}
    
    except:
        return {"error":"true",
                "message":"Please reformat the list"}




def get_answers():
    mydb=defineDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE Answer IS NOT NULL AND NOT Answer = ''")
    myresult = mycursor.fetchall()
    tutors = []
    for x in myresult:
        x[7] #answer
        tutors.append(x[7]) 
    mycursor.close()
    close_db_connection(mydb, "User")
    return tutors


def get_names():
    mydb=defineDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE Answer IS NOT NULL AND NOT Answer = ''")
    myresult = mycursor.fetchall()
    tutors = []
    for x in myresult:
        x[2] #answer
        tutors.append(x[2]) 
    mycursor.close()
    close_db_connection(mydb, "User")
    return tutors


def process_answers():
    return [ast.literal_eval(s) for s in get_answers()]

def get_predictions(list_of_lists):
    # Sample input data for testing
    data = {"instances": list_of_lists}

    # Send a POST request to the TensorFlow Serving REST API
    response = requests.post(os.getenv("cluster_url"), json=data)
    predictions = response.json()

    # Convert predictions to numpy array
    predictions = np.array(predictions["predictions"])

    # Get the indices of the maximum values using argmax
    argmax_indices = np.argmax(predictions, axis=1)

    return argmax_indices
    

def create_name_value_hash(names, values):
    return {name: value for name, value in zip(names, values)}

def parse_answers(hash):
    mydb=defineDB()
    mycursor = mydb.cursor()
    for username, value in hash.items():
        value = int(value)
        mycursor.execute("UPDATE User SET Personality = %s WHERE Nama = %s",(value,username))
    mydb.commit()
    mycursor.close()
        
    close_db_connection(mydb, "User")

def process_user_data():
    answers = process_answers()
    names = get_names()
    predictions = get_predictions(answers)
    name_value_hash = create_name_value_hash(names, predictions)
    parse_answers(name_value_hash)



