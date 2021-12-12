from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.auth.main import authenticate_user, create_jwt_token
import json
from core.auth.model import TokenData
from core.base_model import BaseErrorResponse, BaseResponse
from core.config import settings
from databases.user.model import UserModel, UserSignup
from databases.user.repository import UserRepository

router = APIRouter()

user_repository = UserRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await user_repository.find_user(token_data.email)

    if user is None:
        raise credentials_exception
    return UserModel(**user, id=user["_id"])


@router.get("/user/me/", response_model=UserModel, tags=["user"])
async def read_users_me(current_user: UserModel = Depends(get_current_user)):

    return current_user


@router.post("/auth/signup", tags=["auth", "user"], status_code=status.HTTP_201_CREATED)
async def user_signup(
    response: Response,
    user: UserSignup = Body(...),
):
    user_exist = await user_repository.find_user(user.email)

    if user_exist:
        response.status_code = status.HTTP_409_CONFLICT
        return BaseErrorResponse(message="email_already_exists")

    new_user = await user_repository.add_user(user)
    return BaseResponse(message="success", data=new_user)


@router.post("/auth/login", tags=["auth", "user"])
async def user_login(login_form: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(login_form.username, login_form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_jwt_token(data={"sub": user})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/user/search", tags=["user"])
async def search_user():

    user_exist = await user_repository.find_many()

    users = list(
        map(
            lambda user: {
                "id": str(user["_id"]),
                "email": user["email"],
                "fullname": user["fullname"],
                "phone_number": user["phone_number"],
            },
            user_exist,
        )
    )

    return {"user_exist": users}
