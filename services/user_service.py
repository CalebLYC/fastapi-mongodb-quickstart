from typing import Self
from bson import ObjectId
from fastapi import Depends, HTTPException
from pymongo import ReturnDocument

from dependencies.db_collections import DatabaseCollection
from models.user import CreateUserModel, UpdateUserModel, UserCollectionModel, UserModel
from providers.auth_provider import AuthProvider
from services.token_service import TokenService


class UserService:
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance
    

    _user_collection = DatabaseCollection().user_collection


    #Obtenir la liste de tous les utilisateurs
    async def list_users(self) -> UserCollectionModel:
        try:
            return UserCollectionModel(users = await self._user_collection.find().to_list(length = None))
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting users: {str(e)}")


    #Ajouter un utilisateur à collection
    async def create_user(self, user: CreateUserModel):
        try:
            await self._user_collection.insert_one(
                CreateUserModel(
                    #Décomposer le user en excluant le password puis rajouter le password hashé
                    **user.model_dump(
                        by_alias = True,
                        exclude = ['id', 'password']
                    ),
                    password = AuthProvider.hash_password(user.password) #Password hashé
                ).model_dump(
                    by_alias = True,
                    exclude = ['id']
                )
            )
        except Exception as e:
            raise HTTPException(f"Error while inserting user: {str(e)}")


    #Obtenir un utilisateur à partir de son email
    async def get_user_by_email(self, email: str) -> UserModel:
        try:
            user_data = await self._user_collection.find_one({'email': email})
            if user_data is None:
                return None
            return UserModel(**user_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting user: {str(e)}")


    #Obtenir un utilisateur sous forme de dictionnaire à partir de son email
    async def get_user_data_by_email(self, email: str) -> dict:
        try:
            return await self._user_collection.find_one({'email': email})
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting user: {str(e)}")


    #Obtenir un utilisateur à partir de son id
    async def get_user_by_id(self, id: str) -> UserModel:
        try:
            user_data = await self._user_collection.find_one({'_id': ObjectId(id)})
            if user_data is None:
                return None
            return UserModel(**user_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting user: {str(e)}")


    #Obtenir un utilisateur à partir de son nom
    async def get_user_by_name(self, name: str) -> UserModel:
        try:
            user_data = await self._user_collection.find_one({'name': name})
            if user_data is None:
                return None
            return UserModel(**user_data)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting user: {str(e)}")


    #Récupérer un utilisateur par son jeton d'accès
    async def get_user_by_token(self, token: str) -> UserModel:
        try:
            #Récupérer le document du jeton dans la base de données
            access_token = await TokenService().get_access_token(token)
            if access_token is None:
                raise HTTPException(401, detail = "Not authorized")
            #Récupérer l'utilisateur à partir du user_id du token
            return await self.get_user_by_id(id = access_token.user_id)
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while getting user: {str(e)}")


    #Mettre à jour les données d'un utilisateur
    async def update_user(self, id: str, user: UpdateUserModel) -> UserModel:
        try:
            # Filtrer les attributs du modèle pour ne garder que ceux qui ne sont pas None
            user_data = {
                k: v
                for k, v in user.model_dump(by_alias=True).items()
                if v is not None
            }

            # Vérifiez si le password est dans user_data
            if 'password' in user_data:
                # Hasher le mot de passe
                user_data['password'] = AuthProvider().hash_password(user_data['password'])

            # Vérifiez si user_data n'est pas vide
            if user_data is None:
                raise HTTPException(status_code = 400, detail = "No valid fields provided for update")

            update_result = await self._user_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": user_data},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is None:
                raise HTTPException(status_code = 404, detail = f"User with id {id} not found")
            return update_result     
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while updating user: {str(e)}")


    #Supprimer un utilisateur de la base de données
    async def delete_user(self, id: str):
        try:
            delete_result = await self._user_collection.delete_one({'_id': ObjectId(id)})
            if delete_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"User with id {id} not found")
            return delete_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting user: {str(e)}")


    #Supprimer un utilisateur de la base de données à partir de son email
    async def delete_user_by_email(self, email: str):
        try:
            delete_result = await self._user_collection.delete_one({'email': email})
            if delete_result.deleted_count < 1:
                raise HTTPException(status_code = 404, detail = f"User with email {email} not found")
            return delete_result
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while deleting user: {str(e)}")


    #Ajouter un role à un utilisateur
    async def add_role_to_user(self, id: str, role_name: str):
        try:
            # Récupérer l'utilisateur par son ID
            user = await self.get_user_by_id(id)

            if not user:
                raise HTTPException(status_code = 404, detail = "User not found")

            # Initialiser roles si nécessaire
            if user.roles is None:
                user.roles = []

            # Ajouter le rôle si ce n'est pas déjà présent
            print(user)
            if role_name not in user.roles:
                user.roles.append(role_name)
                await self.update_user(
                    id = user.id,
                    user = UpdateUserModel(**user.model_dump())
                )
            else:
                raise HTTPException(status_code = 400, detail = f"Role {role_name} already assigned")

            return {"detail": "Role added successfully"}

        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while adding role to user: {str(e)}")


    #Ajouter une liste de roles à un tilisateur
    async def add_roles_to_user(self, id: str, role_names: list[str]):
        try:
            # Récupérer l'utilisateur par son ID
            user = await self.get_user_by_id(id)

            if not user:
                raise HTTPException(status_code = 404, detail = "User not found")

            # Initialiser roles si nécessaire
            if user.roles is None:
                user.roles = []

            # Ajouter les rôles s'ils ne sont pas déjà présents
            for role_name in role_names:
                if role_name not in user.roles:
                    user.roles.append(role_name)
                else:
                    raise HTTPException(status_code = 400, detail = f"Role '{role_name}' already assigned")

            # Mettre à jour l'utilisateur
            await self.update_user(
                id = user.id,
                user = UpdateUserModel(**user.model_dump())
            )

            return {"detail": "Roles added successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while adding roles to user: {str(e)}")


    #Supprimer un role à un utilisateur
    async def remove_role_from_user(self, id: str, role_name: str):
        try:
            # Récupérer l'utilisateur par son ID
            user = await self.get_user_by_id(id)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Vérifier si le rôle est présent
            if role_name in user.roles:
                user.roles.remove(role_name)  # Supprimer le rôle
            else:
                raise HTTPException(status_code = 400, detail = f"Role '{role_name}' not assigned")

            # Mettre à jour l'utilisateur
            await self.update_user(
                id = user.id,
                user = UpdateUserModel(**user.model_dump())
            )

            return {"detail": "Role removed successfully"}

        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Error while removing role from user: {str(e)}")



    #Revoquer une liste de roles à un utilisateur
    async def remove_roles_from_user(self, id: str, role_names: list[str]):
        try:
            # Récupérer l'utilisateur par son ID
            user = await self.get_user_by_id(id)

            if not user:
                raise HTTPException(status_code = 404, detail = "User not found")

            # Initialiser une liste pour les rôles manquants
            missing_roles = []

            # Supprimer les rôles s'ils sont présents
            for role_name in role_names:
                if role_name in user.roles:
                    user.roles.remove(role_name)
                else:
                    missing_roles.append(role_name)

            # Mettre à jour l'utilisateur
            await self.update_user(
                id = user.id,
                user=UpdateUserModel(**user.model_dump())
            )

            if missing_roles:
                return {"detail": "Roles removed successfully", "missing_roles": missing_roles}
            return {"detail": "Roles removed successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error while removing roles from user: {str(e)}") 