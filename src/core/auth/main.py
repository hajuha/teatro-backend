from datetime import datetime, timedelta
from core.auth.password import verify_password
from core.config import settings
from databases.user.helper import user_to_dict
from databases.user.repository import UserRepository
from jose import JWTError, jwt

user_repository = UserRepository()

async def authenticate_user(email, password):

    user_exist = await user_repository.find_user(email)

    if not user_exist:
        return False
    if not verify_password(password, user_exist["hashed_password"]):
        return False

    return user_exist["email"]

async def create_jwt_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
