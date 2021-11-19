from fastapi.encoders import jsonable_encoder
from src.core.database.mongo import get_db_client
from src.core.auth.password import get_password_hash
from src.databases.user.helper import user_to_dict
from src.databases.user.model import UserInDB, UserModel


db_client = get_db_client()


class UserRepository:
    def __init__(self):
        self.__user_collection = db_client['teatro']['user']

    async def find_user(self, username: None):

        user_exists = await self.__user_collection.find_one(
            {"username": username}
        )

        if not user_exists:
            return None
        
        return user_exists

    async def add_user(self, user):

        hashed_password= get_password_hash(user.password)

        user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)

        await self.__user_collection.insert_one(jsonable_encoder(user_in_db))

        new_user = await self.__user_collection.find_one({"username": user.username})

        return user_to_dict(new_user)

    async def find_many(self):

        user_exists = self.__user_collection.find()
        if not user_exists:
            return None

        user_to_list = await user_exists.to_list(None)   
        
        return user_to_list