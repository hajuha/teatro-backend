from datetime import datetime, timedelta
from typing import Optional
from src.core.auth.password import verify_password
from src.core.config import Settings
from src.databases.user.helper import user_to_dict
from src.databases.user.repository import UserRepository
from jose import JWTError, jwt

user_repository = UserRepository()

config = Settings()


async def authenticate_user(username, password):

    user_exist = await user_repository.find_user(username)

    if not user_exist:
        return False
    if not verify_password(password, user_exist["hashed_password"]):
        return False

    return user_exist["username"]

async def create_jwt_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(config.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt
