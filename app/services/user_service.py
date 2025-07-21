from app.dto.user_dto import UserActionRequestDto
from app.models import word2vec_util
import numpy as np
from app.models import db_w2v_mapper
from app.repositories.user_weight_repository import UserWeightRepository

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

async def process_user_action(req : UserActionRequestDto, 
                        repo: UserWeightRepository):
    user_id = req.user_id
    # action_type = req.action_type
    # value = req.value

    weights = await repo.find_by_user_id(user_id)
    print(weights)

    # todo 가중중치 업데이트
