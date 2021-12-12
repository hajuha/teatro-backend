from typing import Any, List, Optional
from bson import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.dataclasses import dataclass

from core.base_model import BaseResponse


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


@dataclass
class Ratings:
    customer_id: str
    stars: str


class MovieModel(BaseModel):
    id: PyObjectId = Field(...)
    temp_id: str = Field(...)
    name: str = Field(...)
    release_date: str = Field(...)
    video_release_date: str = Field(...)
    imdb_link: str = Field(...)
    poster_link: str = Field(...)
    tags: List[str] = Field(...)
    ratings: List[Ratings] = Field(...)
    running_time: Optional[int] = Field(...)
    desc: Optional[str] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Movies:
    movies: List[MovieModel] = Field(...)

@dataclass
class SingleMovie:
    id: str
    temp_id: str
    name: str
    release_date: str
    video_release_date: str
    imdb_link: str
    poster_link: str
    tags: List[str]
    ratings: str
    running_time: Optional[int]
    desc: Optional[str]
@dataclass
class RequestUpdateMovie:
    temp_id: str
    name: str
    release_date: str
    video_release_date: str
    imdb_link: str
    poster_link: str
    tags: List[str]
    running_time: Optional[int]
    desc: Optional[str]

class ResponseSingleMovie(BaseResponse):
    data: SingleMovie
class ResponseManyMovies(BaseResponse):
    data: List[SingleMovie]
    
class SearchMovieRequest(BaseModel):
    search_text: str
    name: str
    page: int
    per_page: int
    sort: int
    
    class Config:
        schema_extra = {
            "example": {
                "search_text": "",
                "name": "",
                "page": 0,
                "per_page": 10,
                "sort": 1,
            }
        }
