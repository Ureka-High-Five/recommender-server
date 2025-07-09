from app.repositories import user_repository
from app.repositories import content_repository
from app.models import word2vec_util
from app.settings import settings
import ast

def contents(user_id: str) -> list[str]:
  user_weights = user_repository.user_weight(user_id)
  user_vector = word2vec_util.calc_user_vector(user_weights)
  return find_similar_contents(user_vector) # 모든 contents_vector와 user_vector 비교
  
def shorts(user_id : str) -> list[str]:
  return 0

def find_similar_contents(user_vector):
  content_vectors = content_repository.get_all_vector()

  similarities = []
  for content_id, content_data in content_vectors.items():
    content_vector = content_data['embedding']
    similarity = word2vec_util.calc_similarity(ast.literal_eval(user_vector), ast.literal_eval(content_vector))
    similarities.append({
                      "id": content_id,
                      "title": content_data["title"],
                      "thumbnail": content_data["thumbnail_url"],
                      "score": similarity
                    })

  similarities.sort(key=lambda x: x["score"], reverse=True)
  return similarities[:settings.RECOMMEND_CONTENTS_COUNT]
