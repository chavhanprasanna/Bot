from motor.motor_asyncio import AsyncIOMotorClient

from .config import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None


mongodb = MongoDB()


def connect_to_mongo() -> None:
    if not settings.mongo_uri:
        raise ValueError("MONGO_URI is not set")
    mongodb.client = AsyncIOMotorClient(settings.mongo_uri)


def close_mongo_connection() -> None:
    if mongodb.client:
        mongodb.client.close()


def get_db():
    if not mongodb.client:
        raise RuntimeError("MongoDB client is not initialized")
    return mongodb.client[settings.mongo_db_name]
