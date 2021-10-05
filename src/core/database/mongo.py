import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.core import config

settings = config.Settings()
client = AsyncIOMotorClient(settings.MONGO_URI)

class Database:
    client: AsyncIOMotorClient = None

def get_db_client() -> AsyncIOMotorClient:
    return client
