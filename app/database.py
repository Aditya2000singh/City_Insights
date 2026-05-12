from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import get_settings
import certifi

settings = get_settings()

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client

    if _client is None:
        _client = AsyncIOMotorClient(
            settings.mongodb_url,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,
        )

    return _client


def get_db() -> AsyncIOMotorDatabase:
    return get_client()[settings.mongodb_db_name]


async def close_db():
    global _client

    if _client:
        _client.close()
        _client = None


async def init_db():
    db = get_db()

    await db.snapshots.create_index(
        "fetched_at",
        expireAfterSeconds=60 * 60 * 24 * 15
    )

    await db.snapshots.create_index(
        [("city_id", 1), ("fetched_at", -1)]
    )