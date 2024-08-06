from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status

from dependencies.auth import admin_role_dependency, superadmin_role_dependency
from models.role import RoleCollection, RoleModel
from models.user import UserModel
from services.role_service import RoleService


router = APIRouter(
    prefix = '/roles',
    tags = ['Roles'],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)


@router.get(
    '/',
    status_code = status.HTTP_200_OK,
    response_model = RoleCollection,
    response_model_by_alias = True,
    response_description = "Get all roles",
)
async def get_all_roles(current_user: Annotated[UserModel, Depends(admin_role_dependency)]):
    return await RoleService().list_roles()


@router.post(
    '/',
    status_code = status.HTTP_201_CREATED,
    response_model = RoleModel,
    response_model_by_alias = True,
    response_description = "Add a role",
)
async def add_role(
    current_user: Annotated[UserModel, Depends(superadmin_role_dependency)],
    role: RoleModel = Body(...)
):
    db_role = await RoleService().get_role(role_name = role.name)
    if db_role is not None:
        raise HTTPException(status_code = 400, detail = "Role already exists")
    await RoleService().create_role(role = role)
    return await RoleService().get_role(role_name = role.name)


@router.get(
    '/{name}',
    status_code = status.HTTP_200_OK,
    response_model = RoleModel,
    response_model_by_alias = True,
    response_description = "Get a role",
)
async def show_role(current_user: Annotated[UserModel, Depends(admin_role_dependency)],  name: str):
    return await RoleService().get_role(name)


@router.delete(
    '/{name}',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Delete a role",
)
async def del_role(current_user: Annotated[UserModel, Depends(superadmin_role_dependency)], name: str):
    await RoleService().delete_role(name)
    return  {
        'message': "Roles deleted successfully"
    }


@router.delete(
    '/',
    status_code = status.HTTP_200_OK,
    response_model_by_alias = True,
    response_description = "Delete all roles",
)
async def del_role(current_user: Annotated[UserModel, Depends(superadmin_role_dependency)]):
    await RoleService().delete_roles()
    return  {
        'message': "Roles deleted successfully"
    }