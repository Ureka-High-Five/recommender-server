def recommend_contents_by_user(user_vector, count) -> list[str]:
  return find_similar_contents(user_vector, count)

def find_similar_contents(user_vector, count):
  # all_contents = content_repository.get_all()
  # similarities = []
  # for content_id, content_data in all_contents.items():
  #   content_vector = content_data['embedding']
  #   similarity = word2vec_util.calc_similarity(ast.literal_eval(user_vector), ast.literal_eval(content_vector))
  #   similarities.append({
  #                     "id": content_id,
  #                     "title": content_data["title"],
  #                     "thumbnail": content_data["thumbnail_url"],
  #                     "score": similarity
  #                   })

  # similarities.sort(key=lambda x: x["score"], reverse=True)
  # return similarities[:count]
  data = list(range(1000))
  return [{"id": i} for i in range(420, 420 + count)]
