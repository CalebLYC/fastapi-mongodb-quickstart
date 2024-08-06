from typing import Annotated, List, Optional

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field


PyObjectId = Annotated[str, BeforeValidator(str)]


#Model de base d'un utilisateur
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    email: EmailStr = Field(...)
    name: str = Field(...)
    surname: str = Field(...)
    roles: Optional[List[str]] = Field(default = None)


#Model de création d'un utilisateur incluant le mot de passe
class CreateUserModel(UserModel): 
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_schema_extra = {
            'example': {
                'email': 'jdoe@example.com',
                'name': 'John',
                'surname': 'Doe',
                'password': '12345678'
            }
        }
    )


#Model de mise à jour d'un utilisateur
class UpdateUserModel(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = Field(default = None)
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            'example': {
                'email': 'jdoe@example.com',
                'name': 'John',
                'surname': 'Doe',
                'password': '12345678'
            }
        }
    )


#Model de liste des utilisateurs
class UserCollectionModel(BaseModel):
    users: List[UserModel]