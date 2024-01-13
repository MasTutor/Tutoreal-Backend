#this file for encoding and decoding and returning jwts
import hashlib
import jwt
import time
from decouple import config
from typing import Dict

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

#deez generated tokens (jwts)
def token_response(token: str):
    return{
        "access token": token
    }

def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    token = jwt.encode(payload,JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token:str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time()else None
    except:
        return {}