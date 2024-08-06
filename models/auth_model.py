from typing import Optional
from pydantic import BaseModel

from models.token import AccessTokenModel
from models.user import UserModel


#Model de structuration des données retournés par les endpoints d'authentication
#incluant le jeton d'accès et l'utilisateur authentifié
class AuthModel(BaseModel):
    message: Optional[str] = "Success"
    user_acess_token: AccessTokenModel
    user: UserModel