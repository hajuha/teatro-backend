from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    MONGO_URI:str
    MONGO_USERNAME:str
    MONGO_PASSWORD:str
    SECRET_KEY :str
    ALGORITHM :str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"