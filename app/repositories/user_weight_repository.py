from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import UpdateOne

class UserWeightRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client["highfive"]
        self.collection: AsyncIOMotorCollection = self.db["user_weight"]

    def update_user_weights(
        self, user_id: int, meta_info_ids: list[int], weight: float
    ):
        operations = []
        for meta_id in meta_info_ids:
            operations.append(
                UpdateOne(
                    {"user_id": user_id, "meta_info_id": meta_id},
                    {"$inc": {"weight": weight}},
                    upsert=True,
                )
            )
        if operations:
            self.collection.bulk_write(operations)

    async def find_by_user_id(self, user_id: int) -> List[Dict]:
        cursor = self.collection.find({"userId": user_id})
        results = await cursor.to_list(length=None)
        return results
    
    async def reset_weight(self, user_id: int, genre: str, weight: float):
        filter = {"userId": user_id, "metaInfoName": genre}
        update = {"$set": {"weight": weight}}
        await self.collection.update_one(filter, update, upsert=True)
