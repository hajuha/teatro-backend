from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from core.database.mongo import get_collection, get_db_client
from core.auth.password import get_password_hash
from databases.user.helper import user_to_dict
from databases.user.model import UserInDB, UserModel


class UserRepository:

    async def find_user(self, email: None):
        user_collection = await get_collection('user')

        user_exists = await user_collection.find_one(
            {"email": email}
        )

        if not user_exists:
            return None
        
        return user_exists

    async def add_user(self, user):
        user_collection = await get_collection('user')

        hashed_password= get_password_hash(user.password)
        
        user_in_db = UserInDB(**user.dict(), hashed_password=hashed_password)

        await user_collection.insert_one(jsonable_encoder(user_in_db))

        new_user = await user_collection.find_one({"email": user.email})

        return user_to_dict(new_user)

    async def find_many(self):
        user_collection = await get_collection('user')

        user_exists = user_collection.find()
        if not user_exists:
            return None

        user_to_list = await user_exists.to_list(None)   
        
        return user_to_list