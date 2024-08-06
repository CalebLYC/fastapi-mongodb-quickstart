from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

from dependencies.auth import admin_role_dependency, superadmin_role_dependency
from models.role import AddRoleModel, AddRolesModel
from models.user import CreateUserModel, UpdateUserModel, UserCollectionModel, UserModel
from services.role_service import RoleService
from services.token_service import TokenService
from services.user_service import UserService


router = APIRouter(
    prefix = '/users',
    tags = ['Users'],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)


@router.get(
    '/',
    response_model = UserCollectionModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Get all Users",      
)
async def get_users(current_user: UserModel = Depends(admin_role_dependency)):
    #Récupérer puis retourner tous les utilisateurs
    return await UserService().list_users()


@router.post(
    '/',
    response_model = UserModel,
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = True,
    response_description = "Add a User",      
)
async def add_user(
    current_user: UserModel = Depends(admin_role_dependency),
    user: CreateUserModel = Body(...),
):
    #Vérifier si l'email n'existe pas déjà dans la base de données
    if await UserService().get_user_by_email(user.email) is not None:
        raise HTTPException(status_code = 400, detail = "Email already exists")
    #Stocker l'utilisateur
    await UserService().create_user(user)
    #Récupérer l'utilisateur et son id à partir de son email
    return await UserService().get_user_by_email(user.email)


@router.get(
    '/{id}',
    response_model = UserModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Get a User by id",      
)
async def show_user(id, current_user: UserModel = Depends(admin_role_dependency)):
    #Récupérer l'utilisateur dont l'id se trouve dans le path parameter et le retourner
    user = await UserService().get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user


@router.put(
    '/{id}',
    response_model = UserModel,
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Update a User",      
)
async def edit_user(
    id,
    current_user: UserModel = Depends(admin_role_dependency),
    user: UpdateUserModel = Body(...)
):
    #Récupérer l'utilisateur dont l'id se trouve dans le path parameter
    db_user = await UserService().get_user_by_id(id)
    #Mettre à jour les données de l'utilisateur
    new_user = await UserService().update_user(id = db_user.id, user = user)
    #Supprimer les jetons d'accès de l'utilisateur
    await TokenService().delete_access_token_by_user_id(db_user.id)
    return new_user


@router.delete(
    '/{id}',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Delete a user",
)
async def delete(id, current_user: UserModel = Depends(admin_role_dependency)):
    #Récupérer l'utilisateur dont l'id se trouve dans le path parameter
    user = await UserService().get_user_by_id(id)
    #Supprimer les jetons d'accès de l'utilisateur
    await TokenService().delete_access_token_by_user_id(user.id)
    #Supprimer l'utilisateur
    await UserService().delete_user(user.id)
    return {
        'message': "User deleted successfully"
    }


@router.post(
    '/{id}/role',
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = True,
    response_description = "Add role to a user",
)
async def add_role(
    id,
    current_user: UserModel = Depends(superadmin_role_dependency),
    role_request: AddRoleModel = Body(...)
):
    #Récupérer le document de role
    role = await RoleService().get_role(role_request.role)
    #Vérifier si le role existe dans la base de données
    if role is None:
        raise HTTPException(status_code = 404, detail = "Role not found")
    #Ajouter le role à l'utilisateur
    return await UserService().add_role_to_user(id = id, role_name = role.name)


@router.post(
    '/{id}/roles',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Add a list of roles to a user",
)
async def add_roles(
    current_user: Annotated[UserModel, Depends(superadmin_role_dependency)],
    id: str,
    role_request: AddRolesModel = Body(...)
):
    exists_roles = []
    missing_roles = []
    
    for role in role_request.roles:
        # Récupérer le document de rôle
        db_role = await RoleService().get_role(role)
        
        # Vérifier si le rôle existe dans la base de données
        if db_role is None:
            missing_roles.append(role)
        else:
            exists_roles.append(role)
        
    # Ajouter les rôles existants à l'utilisateur
    await UserService().add_roles_to_user(id = id, role_names = exists_roles)

    return {
        'message': "Request success",
        'roles_added_with_success': exists_roles,
        'missing_roles': missing_roles
    }



@router.delete(
    '/{id}/role',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Remove role to a user",
)
async def remove_role(
    id,
    current_user: UserModel = Depends(superadmin_role_dependency),
    role_request: AddRoleModel = Body(...)
):
    #Récupérer le document de role
    role = await RoleService().get_role(role_request.role)
    #Vérifier si le role existe dans la base de données
    if role is None:
        raise HTTPException(status_code = 404, detail = "Role not found")
    #Révoquer le role à l'utilisateur
    return await UserService().remove_role_from_user(id = id, role_name = role.name)


@router.delete(
    '/{id}/roles',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Remove a list of roles to a user",
)
async def remove_roles(
    id,
    current_user: UserModel = Depends(superadmin_role_dependency),
    role_request: AddRolesModel = Body(...)
):
    #Révoquer la liste de roles à l'utilisateur
    return await UserService().remove_role_from_user(id = id, role_names = role_request.role)