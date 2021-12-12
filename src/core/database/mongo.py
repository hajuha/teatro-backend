import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from core.config import settings

client: AsyncIOMotorClient = None

class Database:
    client: AsyncIOMotorClient = None

async def get_db_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.MONGODB_DATABASE.MONGODB_URI)
    return client

async def get_collection(name: str = 'teatro_collection'):
    client = await get_db_client()
    database = client.teatro
    teatro_collection = database.get_collection(name)
    return teatro_collection


async def close_db():
    """Close database connection."""
    client.close()
