from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    """
    Container for a single user record
    """
    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str
    email: EmailStr
