from typing import Optional
from pydantic.main import BaseModel
from pydantic import Field


class UserModel(BaseModel):
    username: str = Field(...)
    email: Optional[str] = Field(...)
    fullname: Optional[str] = Field(...)
    hashed_password: str = Field(...)

class UserSignup(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "user_0",
                "fullname": "Slim Pro",
                "email": "abdulazeez@x.com",
                "password": "12345678"
            }
        }

class UserInDB(UserModel):
    hashed_password: str