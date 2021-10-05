# from fastapi.routing import APIRouter


# router = APIRouter()

# @router.post("auth/verify")
# async def user_signup():
#     user_exist = await user_repository.find_user(user.username)

#     if user_exist:
#         return "Email already exists"

#     new_user = await user_repository.add_user(user)

#     return new_user