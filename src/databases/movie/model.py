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
class Review:
    CustomerId: str
    Stars: str
    Comment: str


class MovieModel(BaseModel):
    id: str = Field(...)
    TempId: str = Field(...)
    Name: str = Field(...)
    ReleaseDate: str = Field(...)
    VideoReleaseDate: str = Field(...)
    IMDB: str = Field(...)
    Tags: List[str] = Field(...)
    Reviews: List[Review] = Field(...)
    ratings: Optional[int]
    RunningTimeInMinutes: Optional[int] = Field(...)
    Description: Optional[str] = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Movies:
    movies: List[MovieModel] = Field(...)

@dataclass
class SingleMovie:
    id: str
    TempId: str
    Name: str
    ReleaseDate: str
    VideoReleaseDate: str
    IMDB: str
    Tags: List[str]
    ratings: str
    RunningTimeInMinutes: Optional[int]
    Description: Optional[str]
@dataclass
class RequestUpdateMovie:
    TempId: str
    Name: str
    ReleaseDate: str
    VideoReleaseDate: str
    IMDB: str
    Tags: List[str]
    RunningTimeInMinutes: Optional[int]
    Description: Optional[str]

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
