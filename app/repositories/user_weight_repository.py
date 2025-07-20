from typing import List, Dict
from pymongo import MongoClient

class UserWeightRepository:
    def __init__(self, mongo_client: MongoClient):
        self.db = mongo_client["highfive"]
        self.collection = self.db["user_weight"]

    def find_by_user_id(self, user_id: int) -> List[Dict]:
        results = self.collection.find({"userId": user_id})
        return list(results)