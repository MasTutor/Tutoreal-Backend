from cryptography.fernet import Fernet
import os

def password_encryption(password):
    Encrypt_key = bytes(os.getenv("encrypt"),'utf-8')
    f = Fernet(Encrypt_key)
    token = f.encrypt(password)
    return token


def password_decryption(password):
    Encrypt_key = bytes(os.getenv("encrypt"),'utf-8')
    f = Fernet(Encrypt_key)
    token = f.decrypt(password)
    return token
