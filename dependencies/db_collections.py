from typing import Self
from config.database import db


class DatabaseCollection():
    _instance = None
    _db = db

    def __new__(cls, db) -> Self:
        if cls._instance is None:
            cls._instance = super(DatabaseCollection, cls).__new__(cls)
        cls._instance._db = db
        return cls._instance
    
    #Récupérer la collection des utilisateurs
    user_collection = _db.get_collection('users')
    #Récupérer la collection des jetons d'accès
    token_collection = _db.get_collection('user_access_tokens')
    #Récupérer la collection des roles
    role_collection = _db.get_collection('user_roles')
    #Récupérer la collection des permissions
    permission_collection = _db.get_collection('user_permissions')