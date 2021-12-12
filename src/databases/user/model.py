from typing import Optional
from dataclasses import dataclass
from pydantic.main import BaseModel
from pydantic import Field
from bson import ObjectId
from pydantic.networks import EmailStr
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class UserModel(BaseModel):
    email: str = Field(...)
    fullname: Optional[str] = Field(...)
    phone_number: Optional[str] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }     

class UserSignup(BaseModel):
    email: EmailStr = Field(...)
    fullname: Optional[str] = None
    phone_number: Optional[str] = None
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user_0@example.com",
                "fullname": "Slim Pro",
                "phone_number": "09875634623",
                "password": "12345678"
            }
        }

class UserInDB(UserModel):
    hashed_password: str