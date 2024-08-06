from typing import Self
from bson import ObjectId
from fastapi import HTTPException

from models.role import RoleCollection, RoleModel
from dependencies.db_collections import DatabaseCollection
from config.database import db

class RoleService:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(RoleService, cls).__new__(cls)
        return cls._instance
    

    _role_collection = DatabaseCollection(db = db).role_collection


    #Récupérer toute la collection des roles
    async def list_roles(self) -> RoleCollection:
        try:
            return RoleCollection(
                roles = await self._role_collection.find().to_list(length = None)
            )
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error getting roles: {str(e)}")


    #Ajouter un document de role dans la base de données
    async def create_role(self, role: RoleModel):
        try:
            await self._role_collection.insert_one(role.model_dump(by_alias=True, exclude=['id']))
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error inserting role: {str(e)}")


    #Récupérer un document de role dans la base de données
    async def get_role(self, role_name: str) -> RoleModel:
        try:
            role_data =  await self._role_collection.find_one({'name': role_name})
            if role_data is None:
                return None
            return RoleModel(**role_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting role: {str(e)}")


    #Récupérer un document de role dans la base de données à partir de son id
    async def get_role_by_id(self, id: str) -> RoleModel:
        try:
            role_data = await self._role_collection.find_one({'_id': ObjectId(id)})
            if role_data is None:
                return None
            return RoleModel(**role_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting role: {str(e)}")


    #Supprimer un role dans la base de données
    async def delete_role(self, role_name: str):
        try:
            del_result = await self._role_collection.delete_one({'name': role_name})
            if del_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"role with role {role_name} not found")
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting role: {str(e)}")


    #Supprimer un role dans la base de données à partir de son id
    async def delete_role_by_id(self, id: str):
        try:
            del_result = await self._role_collection.delete_one({'_id': ObjectId(id)})
            if del_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"role with id {id} not found")
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting role: {str(e)}")


    #Supprimer tous les roles
    async def delete_roles(self):
        try:
            del_result = await self._role_collection.delete_many({})
            if del_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"No role found to delete")
            return del_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting roles: {str(e)}")