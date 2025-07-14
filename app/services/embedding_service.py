import numpy as np
from app.models import word2vec_util

def calc_by_genre(genres):
  vecs = []
  for name in genres:
    vec = word2vec_util.get_vector(name)  # ex) List[float] or np.ndarray
    if vec is None:
      continue
    vecs.append(np.asarray(vec, dtype=np.float32))

  if not vecs:
      raise ValueError("모든 장르 벡터가 비어 있습니다")

  mean_vec = np.mean(vecs, axis=0)
  return mean_vec
