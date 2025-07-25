import logging
from typing import List, Dict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ASCENDING

class ActionLogRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client["leadme"]
        self.collection: AsyncIOMotorCollection = self.db["action_log"]

    async def find_by_user_id(self, user_id: int) -> List[Dict]:
        cursor = self.collection.find({"userId": user_id})
        return await cursor.to_list(length=None)

    async def find_all_order_by_user_id(self) -> List[Dict]:
        cursor = self.collection.find().sort("userId", ASCENDING)
        return await cursor.to_list(length=None)

    async def mark_status(
            self,
            collection_names: list[str],
            doc_id: str,
            status: str,
            delete_from_secondary: bool = False
    ):
        try:
            primary_collection = self.db[collection_names[0]]
            await primary_collection.update_one(
                {"_id": doc_id},
                {"$set": {"status": status}}
            )

            secondary_collection = self.db[collection_names[1]]

            if delete_from_secondary:
                await secondary_collection.delete_one({"_id": doc_id})
            else:
                await secondary_collection.update_one(
                    {"_id": doc_id},
                    {"$set": {"status": status}}
                )

        except Exception as error:
            print(error)
            logging.error(
                f"[actionlog_status_update_failed] ActionLog 상태 {status} 업데이트 중 예외 발생: id = {doc_id}, error = {error}"
            )
