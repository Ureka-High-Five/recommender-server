from app.enum.action_type import ActionType
from app.models import word2vec_util
import numpy as np
from app.models import db_w2v_mapper
from app.repositories.user_weight_repository import UserWeightRepository
from app.repositories.action_log_repository import ActionLogRepository
from app.services.redis import save_user_vector
from app.services.weight_strategy import convert_to_weight


def init_user_vector(genre_map):
    weighted_vectors = []
    total_weight = 0

    for genre, weight in genre_map.items():
        genre = db_w2v_mapper.translate_genre(genre)
        vector = word2vec_util.get_vector(genre)
        if vector is None:
            continue
        weighted_vectors.append(np.array(vector) * weight)
        total_weight += weight

    if not weighted_vectors or total_weight == 0:
        return str([0.0] * 300)

    user_vector = sum(weighted_vectors) / total_weight
    return str(user_vector.tolist())


async def process_user_action(message: dict, userRepo: UserWeightRepository, actionLogRepo:ActionLogRepository):
    user_id = message.get("userId")
    meta_info_names = message.get("metaInfoNames", [])
    action_type = ActionType[message.get("actionType")]
    value = message.get("value", 0.0)

    weight_from_message = convert_to_weight(action_type, value)

    weights = await userRepo.find_by_user_id(user_id)

    db_weight_map = {doc.get("name"): doc.get("weight", 0.0) for doc in weights}
    combined_weights = {}

    for name in meta_info_names:
        existing_weight = db_weight_map.get(name, 0.0)
        combined_weights[name] = existing_weight + weight_from_message

    user_vector = word2vec_util.calc_user_vector(combined_weights)
    user_vector_str = np.array2string(user_vector, separator=', ')
    await save_user_vector(user_id, user_vector_str)
    await actionLogRepo.mark_status(collection_names=["action_log", "managed_action_log"],
                                                       doc_id=message["id"], status="SUCCESS",
                                                       delete_from_secondary=True)


async def update_user_weight(message: dict, repo: UserWeightRepository):
    user_id = message.get("userId")
    meta_info_ids = message.get("metaInfoIds", [])
    meta_info_names = message.get("metaInfoNames", [])
    action_type = ActionType[message.get("actionType")]
    value = message.get("value", 0.0)

    weight = convert_to_weight(action_type, value)

    if not user_id or not meta_info_ids:
        print("Invalid message:", message)
        return

    meta_info = list(zip(meta_info_ids, meta_info_names))
    repo.update_user_weights(user_id, meta_info, weight)
    print(f" 유저의 가중치 업데이트 성공 : {user_id}")

async def rollback_user_weight(message: dict, repo: UserWeightRepository):
    user_id = message.get("userId")
    meta_info_ids = message.get("metaInfoIds", [])
    meta_info_names = message.get("metaInfoNames", [])
    action_type = ActionType[message.get("actionType")]
    value = message.get("value", 0.0)

    rollback_weight = -1 * convert_to_weight(action_type, value)

    meta_info = list(zip(meta_info_ids, meta_info_names))
    await repo.update_user_weights(user_id, meta_info, rollback_weight)
    print(f" 유저 가중치 롤백 완료: {user_id}")