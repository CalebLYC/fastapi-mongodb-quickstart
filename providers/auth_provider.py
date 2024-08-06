import datetime
from typing import Self
import bcrypt
from fastapi import HTTPException
import jwt

from config.enviro import env


class AuthProvider:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(AuthProvider, cls).__new__(cls)
        return cls._instance


    #Générer un jeton d'accès
    def create_user_access_token(data: dict, expires_delta: datetime.timedelta = None) -> str:
        try:
            return jwt.encode(data, env('SECRET_KEY'), algorithm=env('ALGORITHM'))
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error creating access token: {str(e)}")


    #Hasher un mot de passe
    def hash_password(password: str) -> str:
        try:
            return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf-8')
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error hashing password: {str(e)}")


    #Vérifier un mot de passe
    def check_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(plain_password.encode('utf8'), hashed_password.encode('utf8'))
        except:
            raise HTTPException(status_code = 400, detail = "Bad credentials")