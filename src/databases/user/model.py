from typing import Optional
from pydantic.main import BaseModel
from pydantic import Field
from bson import ObjectId
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
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str = Field(...)
    email: Optional[str] = Field(...)
    fullname: Optional[str] = Field(...)
    hashed_password: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }     

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