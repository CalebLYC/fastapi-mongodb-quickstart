from typing import Annotated, List
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.user import UserModel
from services.user_service import UserService


#Définir la dépendance de l'entête Authorization
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

"""
    Récupérer l'utilisateur à partir du token défini dans l'entête Authorization
    Dépendance permettant d'authenifier l'utilisateur qui envoie la requête
"""
async def auth_dependency(token: str = Depends(oauth_2_scheme)) -> UserModel:
    current_user = await UserService().get_user_by_token(token)
    if current_user is None:
        raise HTTPException(401, detail = "Not authorized")
    return current_user


#Dépendance lié à une liste rôles dont l'utilisateur envoyant la requête doit en avoir une
async def verify_roles(roles: List[str], current_user: UserModel = Depends(auth_dependency)) -> UserModel:
    #Vérifier si les roles existent
    if current_user.roles is not None:
        # Vérifier si l'utilisateur a au moins un des rôles requis
        if any(role in current_user.roles for role in roles):
            return current_user
    raise HTTPException(status_code = 401, detail = "Not authorized")


#Dépendance lié à une liste rôles dont l'utilisateur envoyant la requête doit en avoir une
async def admin_role_dependency(current_user: UserModel = Depends(auth_dependency)) -> UserModel:
    if current_user.roles is not None:
        #Définir la liste des roles
        roles = ["admin", "superadmin"]
        # Vérifier si l'utilisateur a au moins un des rôles requis
        if any(role in current_user.roles for role in roles):
            return current_user
    raise HTTPException(status_code = 401, detail = "Not authorized")


#Dépendance lié à une liste rôles dont l'utilisateur envoyant la requête doit en avoir une
async def superadmin_role_dependency(current_user: UserModel = Depends(auth_dependency)) -> UserModel:
    if current_user.roles is not None:
        #Définir la liste des roles
        roles = ["superadmin"]
        # Vérifier si l'utilisateur a au moins un des rôles requis
        if any(role in current_user.roles for role in roles):
            return current_user
    raise HTTPException(status_code = 401, detail = "Not authorized")