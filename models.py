from typing import Annotated, List
from pydantic import BaseModel, Field, EmailStr, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    """
    Container for a single user record
    """
    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str
    email: EmailStr


class UserCollection(BaseModel):
    users: List[UserModel]


class UpdateUserModel(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
