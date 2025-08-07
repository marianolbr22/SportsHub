from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class MongoDB:
    _client: Optional[AsyncIOMotorClient] = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient("mongodb+srv://otrousuario:otracontrase%C3%B1a@cluster0.ohyaf.mongodb.net/")
        return cls._client

    @classmethod
    def get_database(cls, db_name: str = "Pruebas") -> AsyncIOMotorClient:
        client = cls.get_client()
        return client[db_name]
