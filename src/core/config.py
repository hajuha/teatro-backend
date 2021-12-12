from enum import unique
from pydantic import BaseSettings
from pydantic.main import BaseModel
from pydantic.fields import Field

from core.types import ExtendedEnum

class MongoDBConnectionOptions(BaseModel):

    MIN_POOL_SIZE: int = Field(...)
    MAX_POOL_SIZE: int = Field(...)
    
@unique
class StatusCodeEnum(int, ExtendedEnum):

    success = 1
    failed = 0


class MongoDBDatabase(BaseModel):

    DATABASE_NAME: str = Field(...)
    PASSWORD: str = Field(...)

    USER: str = Field(...)
    HOST: str = Field(...)
    PORT: int = Field(...)

    REPLICASET: str = Field(...)

    CONN_OPTS: MongoDBConnectionOptions

    COLLECTIONS: dict = {
        "user": {
            "name": "user"
        },
        "movie": {
            "name": "movie"
        },
        "cinema": {
            "name": "cinema"
        },
        "showtime": {
            "name": "showtime"
        }
    }

    @property
    def MONGODB_URI(self):

        return 'mongodb://{}:{}/{}?replicaSet={}'.format(
            # self.USER,
            # self.PASSWORD,
            self.HOST,
            self.PORT,
            self.DATABASE_NAME,
            self.REPLICASET
        )

MESSAGES = {
    "success": "success",
    "failed": "failed",
    "unauthorized": "unauthorized",
    "inactive_user": "inactive_user",
    "email_already_exists": "email_already_exists",
    "movie_not_found": "movie_not_found",
}

class Pagination(BaseModel):

    MAX_PER_PAGE = 10
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 5

class Settings(BaseSettings):
    APP_NAME: str = "Teatro"
    MONGODB_DATABASE: MongoDBDatabase
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "Teatro"
    PAGINATION: Pagination = Pagination()

    class Config:
        env_file = ".env"


settings = Settings()
