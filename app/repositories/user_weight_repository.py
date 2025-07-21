from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

class UserWeightRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client["highfive"]
        self.collection: AsyncIOMotorCollection = self.db["user_weight"]

    async def find_by_user_id(self, user_id: int) -> List[Dict]:
        cursor = self.collection.find({"userId": user_id})
        results = await cursor.to_list(length=None)
        return results
