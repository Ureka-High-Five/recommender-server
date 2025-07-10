from app.models import word2vec_util
import numpy as np

def init_user_vector(genre_map):
    weighted_vectors = []
    total_weight = 0

    for genre, weight in genre_map.items():
        vector = word2vec_util.get_vector(genre)
        if vector is None:
            continue
        weighted_vectors.append(np.array(vector) * weight)
        total_weight += weight

    if not weighted_vectors or total_weight == 0:
        return str([0.0] * 300)

    user_vector = sum(weighted_vectors) / total_weight
    return str(user_vector.tolist())