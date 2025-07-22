from app.dto.user_dto import UserActionRequestDto
from app.enum.action_type import ActionType
from app.models import word2vec_util
import numpy as np
from app.models import db_w2v_mapper
from app.repositories.user_weight_repository import UserWeightRepository
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


async def process_user_action(message: dict, repo: UserWeightRepository):
    user_id = message.get("userId")
    meta_info_names = message.get("metaInfoNames", [])
    action_type = ActionType[message.get("actionType")]
    value = message.get("value", 0.0)

    weight_from_message = convert_to_weight(action_type, value)

    weights = await repo.find_by_user_id(user_id)

    db_weight_map = {doc.get("name"): doc.get("weight", 0.0) for doc in weights}

    # 기존 가중치와 메시지에서 받은 가중치를 합산
    combined_weights = {}

    for name in meta_info_names:
        existing_weight = db_weight_map.get(name, 0.0)
        combined_weights[name] = existing_weight + weight_from_message

    user_vector = word2vec_util.calc_user_vector(combined_weights)

    print(user_vector)


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
