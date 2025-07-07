import numpy as np
from models.word2vec_model import Word2VecModel

def calc_user_vector(user_weights):
  weighted_vectors = []
  for name, weight in user_weights.items():
    try:
      vector = Word2VecModel.get_vector(name)
      weighted_vectors.append(vector * weight)
    except KeyError:
      print(f"[WARN] '{name}' 벡터 없음, 스킵")
      continue

  if not weighted_vectors:
    return []  # 벡터가 하나도 없을 경우

  avg_vector = np.mean(weighted_vectors, axis=0)  # 평균 벡터 계산

  return avg_vector

