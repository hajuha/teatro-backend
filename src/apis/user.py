from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.auth.main import authenticate_user, create_jwt_token
import json
from src.databases.user.model import UserModel, UserSignup
from src.databases.user.repository import UserRepository

router = APIRouter()

user_repository = UserRepository()


@router.post("/auth/signup")
async def user_signup(user: UserSignup = Body(...)):
    user_exist = await user_repository.find_user(user.username)

    if user_exist:
        return "Email already exists"

    new_user = await user_repository.add_user(user)

    return new_user


@router.post("/auth/login")
async def user_login(login_form: OAuth2PasswordRequestForm = Depends()):

    print(login_form)

    user = await authenticate_user(login_form.username, login_form.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_jwt_token(data={"sub": user})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/user/search")
async def search_user():

    user_exist = await user_repository.find_many()
    
    users = list(
        map(
            lambda user: {
                "id": str(user['_id']),
                "username": user['username'],
                "email": user['email'],
                "fullname": user['fullname'],
            },
            user_exist,
        )
    )

    return {"user_exist": users}
