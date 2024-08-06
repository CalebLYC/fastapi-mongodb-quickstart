from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

from dependencies.auth import auth_dependency
from models.auth_model import AuthModel
from models.token import AccessTokenModel
from models.user import CreateUserModel, UpdateUserModel, UserModel
from providers.auth_provider import AuthProvider
from services.token_service import TokenService
from services.user_service import UserService


router = APIRouter(
    tags = ['Auth'],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)


@router.post(
    '/register',
    response_model = AuthModel,
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = True,
    response_description = "Register User",      
)
async def register(user: CreateUserModel = Body(...)):
    #Vérifier si l'email n'existe pas déjà dans la base de données
    if await UserService().get_user_by_email(user.email) is not None:
        raise HTTPException(status_code = 400, detail = "Email already exists")
    #Stocker l'utilisateur
    await UserService().create_user(user)
    #Récupérer l'utilisateur et son id à partir de son email
    new_user = await UserService().get_user_by_email(user.email)
    #Générer le jeton d'accès
    token = AuthProvider.create_user_access_token({'sub': user.email})
    #Stoker le jeton d'accès
    access_token = AccessTokenModel(token = token, user_id = new_user.id)
    #Récupérer le document du jeton d'accès
    await TokenService().add_access_token(access_token = access_token)
    access_token = await TokenService().get_access_token(token)
    #Retourner le jeton d'accès et l'utilisateur associé
    return AuthModel(
        message = "User registered successfully",
        user_acess_token = access_token,
        user = new_user
    )


@router.post(
    '/login',
    response_model = AuthModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Register User",      
)
async def login(email: str = Body(...), password: str = Body(...)):
    user = await UserService().get_user_data_by_email(email)
    if user is  None:
        raise HTTPException(status_code = 401, detail = "Bad credentials")
    if not AuthProvider.check_password(password, user['password']):
        raise HTTPException(status_code = 401, detail = "Bad credentials")
    #Générer le jeton d'accès
    token = AuthProvider.create_user_access_token({'sub': user['email']})
    #Stoker le jeton d'accès
    access_token = AccessTokenModel(token = token, user_id = user['_id'])
    #Récupérer le document du jeton d'accès
    await TokenService().add_access_token(access_token = access_token)
    access_token = await TokenService().get_access_token(token)
    #Retourner le jeton d'accès et l'utilisateur associé
    return AuthModel(message = "User logged succesfully", user_acess_token = access_token, user = user)


@router.get(
    '/current',
    response_model = UserModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Get current User",      
)
async def get_auth_current_user(current_user: Annotated[UserModel, Depends(auth_dependency)]):
    return current_user


@router.put(
    '/current',
    response_model = AuthModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Update current User",      
)
async def update_current_user(
    current_user: Annotated[UserModel, Depends(auth_dependency)],
    user: UpdateUserModel = Body(...)
):
    #Mettre à jour les données de l'utilisateur
    new_user = await UserService().update_user(id = current_user.id, user = user)
    #Supprimer les jetons de l'utilisateur
    await TokenService().delete_access_token_by_user_id(new_user.id)
    #Générer un nouveau jeton d'accès
    token = AuthProvider.create_user_access_token({'sub': new_user['email']})
    #Stoker le jeton d'accès
    access_token = AccessTokenModel(token = token, user_id = new_user.id)
    #Récupérer le document du jeton d'accès
    await TokenService().add_access_token(access_token = access_token)
    access_token = await TokenService().get_access_token(token)
    #Retourner le jeton d'accès et l'utilisateur associé
    return AuthModel(
        message = "User updated successfully",
        user = new_user,
        user_acess_token = access_token,
    )


@router.put(
    '/current/password',
    response_model = AuthModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Update current User password",      
)
async def update_current_user_password(
    current_user: Annotated[UserModel, Depends(auth_dependency)],
    old_password: str = Body(...),
    new_password: str = Body(...)
):
    #Récupérer l'utilisateur avec son mot de passe
    user = await UserService().get_user_data_by_email(current_user.email)
    #Vérifier l'ancien mot de passe
    if not AuthProvider.check_password(old_password, user['password']):
        raise HTTPException(status_code = 401, detail = "Wrong old password")
    #Mettre à jour le password de l'utilisateur
    user['password'] = new_password
    new_user = await UserService().update_user(id = current_user.id, user = UpdateUserModel(**user))
    #Supprimer les jetons de l'utilisateur
    await TokenService().delete_access_token_by_user_id(new_user.id)
    #Générer un nouveau jeton d'accès
    token = AuthProvider.create_user_access_token({'sub': f"{new_user['name']}{new_user.surname}",})
    #Stoker le jeton d'accès
    access_token = AccessTokenModel(token = token, user_id = new_user.id)
    #Récupérer le document du jeton d'accès
    await TokenService().add_access_token(access_token = access_token)
    access_token = await TokenService().get_access_token(token)
    #Retourner le jeton d'accès et l'utilisateur associé
    return AuthModel(
        message = "User's password updated successfully",
        user = new_user,
        user_acess_token = access_token,
    )


@router.delete(
    '/logout',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Logout current User",      
)
async def logout(current_user: Annotated[UserModel, Depends(auth_dependency)]):
    del_result = await TokenService().delete_access_token_by_user_id(current_user.id)
    if del_result.deleted_count < 0:
        raise HTTPException(status_code = 404, detail = "User not found")
    return {
        'message': "User logout successfully",
    }


@router.put(
    '/current/email/confirm',
    response_model = UserModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Confirm current user email",      
)
async def confirm_current_user_email(
    current_user: Annotated[UserModel, Depends(auth_dependency)],
    email: str = Body(...)
):
    return current_user


@router.put(
    '/current/password/recover',
    response_model = UserModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Recover current user password",      
)
async def recover_current_user_password(
    current_user: Annotated[UserModel, Depends(auth_dependency)],
    email: str = Body(...)
):
    return current_user


@router.delete(
    '/current',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Delete account",      
)
async def delete(current_user: Annotated[UserModel, Depends(auth_dependency)]):
    #Supprimer les jetons d'accès de l'utilisateur authentifié
    await TokenService().delete_access_token_by_user_id(current_user.id)
    #Supprimer l'utilisateur
    await UserService().delete_user(current_user.id)
    return {
        'message': "Account deleted successfully"
    }