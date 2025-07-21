from typing import List, Dict
from pymongo import MongoClient, UpdateOne


class UserWeightRepository:
    def __init__(self, mongo_client: MongoClient):
        self.db = mongo_client["highfive"]
        self.collection = self.db["user_weight"]

    def find_by_user_id(self, user_id: int) -> List[Dict]:
        results = self.collection.find({"userId": user_id})
        return list(results)

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
