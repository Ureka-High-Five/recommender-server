import logging
from typing import List, Dict

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import UpdateOne

from app.models import db_w2v_mapper


class UserWeightRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.db = mongo_client["leadme"]
        self.collection: AsyncIOMotorCollection = self.db["user_weight"]

    async def update_user_weights(
        self, user_id: int, meta_info: list[tuple[int, str, str]], weight: float
    ):

        meta_info_ids = [meta_id for meta_id, _, _ in meta_info]

        try:  # 1. 기존 값 백업
            original_map = await self.backup_original_weights(user_id, meta_info_ids)
        except Exception as e:
            logging.error(f"[백업 실패] user_id={user_id} - {e}")
            raise

        operations = self.build_update_operations(
            user_id, meta_info, weight
        )  # 2. 업데이트 연산 생성

        try:  # 3. 업데이트 시도
            if operations:
                await self.collection.bulk_write(operations)
                logging.info(f"[가중치 업데이트 성공] user_id={user_id}")
        except Exception as e:
            logging.error(f"[업데이트 실패 - 롤백 시작] user_id={user_id} - {e}")
            await self.rollback_weights(user_id, meta_info, original_map)
            raise  # 로그를 남길 수 있도록 예외 throw 처리

    async def backup_original_weights(
        self, user_id: int, meta_info_ids: list[int]
    ) -> dict:
        cursor = self.collection.find(
            {"user_id": user_id, "meta_info_id": {"$in": meta_info_ids}}
        )
        docs = await cursor.to_list(length=None)
        return {doc["meta_info_id"]: doc.get("weight", 0.0) for doc in docs}

    def build_update_operations(
        self, user_id: int, meta_info: list[tuple[int, str, str]], weight: float
    ):
        ops = []
        for meta_id, name, meta_type in meta_info:
            translated_name = db_w2v_mapper.translate_genre(name)
            ops.append(
                UpdateOne(
                    {
                        "user_id": user_id,
                        "meta_info_id": meta_id,
                    },
                    {
                        "$inc": {"weight": weight},
                        "$set": {"name": translated_name, "type": meta_type},
                    },
                    upsert=True,
                )
            )
        return ops

    async def rollback_weights(
        self, user_id: int, meta_info: list[tuple[int, str, str]], original_map: dict
    ):
        rollback_ops = []
        for meta_id, name, meta_type in meta_info:
            if meta_id not in original_map:
                continue
            translated = db_w2v_mapper.translate_genre(name)
            rollback_ops.append(
                UpdateOne(
                    {"user_id": user_id, "meta_info_id": meta_id},
                    {
                        "$set": {
                            "weight": original_map[meta_id],
                            "name": translated,
                            "type": meta_type,
                        }
                    },
                    upsert=True,
                )
            )

        if rollback_ops:
            try:
                await self.collection.bulk_write(rollback_ops)
                logging.info(f"[롤백 완료] user_id={user_id}")
            except Exception as rollback_err:
                logging.error(f"[롤백 실패] user_id={user_id} - {rollback_err}")
                raise  # 예외 던지기
        raise RuntimeError(
            f"[업데이트 실패로 인한 롤백 후 예외 재전파] user_id={user_id}"
        )

    async def find_by_user_id(self, user_id: int) -> List[Dict]:
        cursor = self.collection.find({"user_id": user_id})
        results = await cursor.to_list(length=None)
        return results

    async def reset_weight(self, user_id: int, genre: str, weight: float):
        filter = {"user_id": user_id, "name": genre}
        update = {"$set": {"weight": weight}}
        await self.collection.update_one(filter, update, upsert=True)
