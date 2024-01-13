import requests
import numpy as np
from decouple import config
from dotenv import load_dotenv
from fastapi import FastAPI, Body, Depends, File, UploadFile, Request
from fastapi.responses import FileResponse
from api.auth.jwt_bearer import jwtBearer
from api.auth.jwt_handler import *
from google.cloud import storage
from dotenv import load_dotenv
from api.encryptor import *
from api.model import *
from io import BytesIO
from api.function import *
from api.db import *
import requests
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

def get_data_as_dataframe(table_name):
    mydb = defineDB()
    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT * FROM {table_name}")
    rows = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    df = pd.DataFrame(rows, columns=column_names)

    mycursor.close()
    mycursor = mydb.cursor()
    close_db_connection(mydb, table_name)

    return df

def get_user_as_dataframe(email):
    mydb = defineDB()
    mycursor = mydb.cursor()
    resq = (email,)
    mycursor.execute("SELECT * FROM User WHERE Email = %s", resq)
    rows = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]
    df = pd.DataFrame(rows, columns=column_names)

    mycursor.close()
    mycursor = mydb.cursor()
    close_db_connection(mydb,'User')

    return df


def process_data(user_df, tutor_df):
    user_df = pd.merge(user_df, tutor_df[['Nama', 'Categories']], on='Nama', how='left')
    user_df = user_df[user_df['Tipe'] != 'student']
    df_name_answers = user_df[['uid', 'Nama', 'hasPenis', 'Answer', 'Personality']]
    match_df = df_name_answers.dropna(subset=['uid', 'Nama', 'hasPenis', 'Answer', 'Personality',])

    df_type = match_df[['Personality']]
    persona_type = pd.get_dummies(df_type, columns=['Personality']).astype(int)
    match_df = match_df.drop(['Answer', 'Personality', 'uid'], axis=1)

    match_df = pd.concat([match_df, persona_type], axis=1)

    # Insert new columns
    new_columns = ['Technology', 'Arts', 'Multimedia', 'Music', 'Science', 'Social', 'Language', 'Math']
    for col in new_columns:
        match_df[col] = None

    # Merge and update categories
    merged_df = pd.merge(match_df, tutor_df[['Nama', 'Categories']], on='Nama', how='left')
    for category in new_columns:
        merged_df[category] = merged_df.apply(lambda row: 1 if row['Categories'] == category else 0, axis=1)
    credentials_df = merged_df['Nama']
    merged_df.drop(['Categories', 'Nama'], axis=1, inplace=True)

    return merged_df, credentials_df

def process_data_user(user_df, user_chosen_category):
    # Keep only relevant columns and drop NA values
    relevant_df = user_df[['hasPenis', 'Personality']].dropna()

    # Ensure Personality column is of float type for consistent encoding
    relevant_df['Personality'] = relevant_df['Personality'].astype(float)

    # Initialize all category columns to 0
    categories = ['Technology', 'Arts', 'Multimedia', 'Music', 'Science', 'Social', 'Language', 'Math']
    for category in categories:
        relevant_df[category] = 0

    # Set the user chosen category to 1
    if user_chosen_category in categories:
        relevant_df[user_chosen_category] = 1

    # Explicitly create columns for each personality type
    personality_types = [0.0, 1.0, 2.0, 3.0, 4.0]
    for p_type in personality_types:
        column_name = f'Personality_{p_type}'
        relevant_df[column_name] = relevant_df['Personality'].apply(lambda x: 1 if x == p_type else 0)

    # Drop the original Personality column
    final_df = relevant_df.drop('Personality', axis=1)

    return final_df


def get_predictions(data):
    response = requests.post(os.getenv("pca_url"), json=data)
    return response.json()



def matchmaking(data, user_key='USER_KEY'):
    # Extract the predictions for USER_KEY
    user_key_prediction = None
    for name, prediction in data:
        if name == user_key:
            user_key_prediction = prediction
            break

    # Check if USER_KEY was found
    if user_key_prediction is None:
        return "USER_KEY not found in the data."

    # Calculate Euclidean distances
    distances = {}
    for name, prediction in data:
        if name != user_key:
            distance = euclidean_distances([user_key_prediction], [prediction])[0][0]
            distances[name] = distance
            
    sorted_data = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])[:5]}
    tutor = []
    for name in sorted_data.keys():
        tutor.append(get_tutor_by_name(name))
    
    return tutor


def master_function(email, category):
    user_data = pd.DataFrame(['USER_KEY'])
    user_df = get_data_as_dataframe("User")
    tutor_df = get_data_as_dataframe("Tutor")
    merged_df, _ = process_data(user_df, tutor_df)
    _, name_df = process_data(user_df, tutor_df)
    name_df = pd.concat([user_data, name_df]).reset_index(drop=True)
    name_d = name_df.iloc[:,0].tolist()

    input_data = process_data_user(get_user_as_dataframe(email), category)
    input_arr = input_data.values
    match_arr = merged_df.values
    one_array_resize = np.reshape(match_arr, (1, -1)) if match_arr.ndim == 1 else match_arr

    data = {"instances": input_arr.tolist() + one_array_resize.tolist()}

    predictions = get_predictions(data)
    combined_data = list(zip(name_d, predictions['predictions']))


    return {
        "error":"false",
        "message": "successfully getting the match XD",
        "data":matchmaking(combined_data)
            }