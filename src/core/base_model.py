from dataclasses import dataclass, field
from typing import Any, Optional
from pydantic.class_validators import root_validator
from pydantic import Field
from pydantic.main import BaseModel
from core.config import MESSAGES, StatusCodeEnum


class BaseResponse(BaseModel):
    code: StatusCodeEnum = StatusCodeEnum.success.value
    message: str = Field(...)
    data: Any

    @root_validator(pre=True)
    def validate(cls, values):

        if not values["message"] in MESSAGES.values():
            raise ValueError("Message invalid")

        return values
    
class BaseErrorResponse(BaseModel):
    code: StatusCodeEnum = StatusCodeEnum.failed.value
    message: str = Field(...)

    @root_validator(pre=True)
    def validate(cls, values):

        if not values["message"] in MESSAGES.values():
            raise ValueError("Message invalid")

        return values

class Pagination(BaseModel):

    skip: Optional[int]
    limit: Optional[int]
    page: Optional[int]


class DataWithPagination(BaseModel):

    data: Any
    total_entries: int
    per_page: Optional[int]
    page: Optional[int]
