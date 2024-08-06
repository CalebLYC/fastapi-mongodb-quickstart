from typing import Annotated, Optional
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObcjectId = Annotated[str, BeforeValidator(str)]


#Model de base de stokage d'un jeton d'accès
class AccessTokenModel(BaseModel):
    id: Optional[PyObcjectId] = Field(alias = '_id', default = None)
    token: str = Field(...)
    user_id: PyObcjectId = Field(...)
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_schema_extra = {
            'example': {
                'token': 'access_token',
                'user_id': '60d5ec49a4b4c3e7b4f4e3b2',
            }
        }
    )


#Model de base de stokage d'un jeton d'accès
class UpdateAccessTokenModel(BaseModel):
    token: Optional[str] = None
    user_id: Optional[PyObcjectId]  = None
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            'example': {
                'token': 'access_token',
                'user_id': '60d5ec49a4b4c3e7b4f4e3b26',
            }
        }
    )