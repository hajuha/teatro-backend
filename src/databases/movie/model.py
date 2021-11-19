from typing import List, Optional
from bson import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel

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


class MovieModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    temp_id: str = Field(...)
    name: str = Field(...)
    release_date: str = Field(...)
    video_release_date: str = Field(...)
    imdb_link: str = Field(...)
    tags: List(str) = Field(...)
    ratings: List(str) = Field(...)
    running_time: Optional[int] = Field(...)
    desc: Optional[str] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }  