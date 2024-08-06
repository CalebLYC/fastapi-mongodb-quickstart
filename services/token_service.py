from typing import Self
from bson import ObjectId
from fastapi import HTTPException

from models.token import AccessTokenModel
from dependencies.db_collections import DatabaseCollection
from config.database import db


class TokenService:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(TokenService, cls).__new__(cls)
        return cls._instance
    

    _token_collection = DatabaseCollection(db = db).token_collection


    #Ajouter un document de token dans la base de données
    async def add_access_token(self, access_token: AccessTokenModel):
        try:
            await self._token_collection.insert_one({
                **access_token.model_dump(by_alias=True, exclude=['id', 'user_id']),
                'user_id': ObjectId(access_token.user_id)
            })
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error inserting token: {str(e)}")


    #Récupérer un document de token dans la base de données
    async def get_access_token(self, token: str) -> AccessTokenModel:
        try:
            token_data =  await self._token_collection.find_one({'token': token})
            if token_data is None:
                return None
            return AccessTokenModel(**token_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting token: {str(e)}")


    #Récupérer un document de token dans la base de données à partir de son id
    async def get_access_token_by_id(self, id: str) -> AccessTokenModel:
        try:
            token_data = await self._token_collection.find_one({'_id': ObjectId(id)})
            if token_data is None:
                return None
            return AccessTokenModel(**token_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting token: {str(e)}")


    #Supprimer un jeton d'accès dans la base de données
    async def delete_access_token(self, token: str):
        try:
            del_result = await self._token_collection.delete_one({'token': token})
            if del_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"Token with token {token} not found")
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting token: {str(e)}")


    #Supprimer un jeton d'accès dans la base de données à partir de son id
    async def delete_access_token_by_id(self, id: str):
        try:
            del_result = await self._token_collection.delete_one({'_id': ObjectId(id)})
            if del_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"Token with id {id} not found")
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting token: {str(e)}")


    #Supprimer un jeton d'accès dans la base de données à partir de son id
    async def delete_access_token_by_user_id(self, user_id: str):
        try:
            del_result = await self._token_collection.delete_many({'user_id': ObjectId(user_id)})
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting token: {str(e)}")


    #Supprimer tous les jetons d'accès
    async def delete_access_tokens(self):
        try:
            del_result = await self._token_collection.delete_many({})
            if del_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"No token found to delete")
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting tokens: {str(e)}")