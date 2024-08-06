from typing import Annotated, List, Optional
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObjectId = Annotated[str, BeforeValidator(str)]


#Model d'un document role
class RoleModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias = '_id', default = None)
    name: str = Field(...)
    description: str = Field(...)
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_schema_extra = {
            'example': {
                'name': 'simple_user',
                'description': 'A simple user',
            }
        }
    )


#Model d'objet permettant de mettre à jour un document de role
class UpdateRoleModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            'example': {
                'name': 'simple_user',
                'description': 'A simple user',
            }
        }
    )


#Model représentant une collection de documents de role
class RoleCollection(BaseModel):
    roles: List[RoleModel]


#Model d'ajout/suppression d'un role à un Utilisateur
class AddRoleModel(BaseModel):
    role: str = Field(...)


#Model d'ajout/suppression d'une liste de roles à un Utilisateur
class AddRolesModel(BaseModel):
    roles: str = Field(...)