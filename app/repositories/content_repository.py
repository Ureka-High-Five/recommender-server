import json
from app.db import get_connection
from app.models import db_w2v_mapper, word2vec_util
from collections import defaultdict
import numpy as np

def get_all_vector() -> dict[str, str]:
  with get_connection() as conn:
    with conn.cursor() as cursor:
      sql = """
            SELECT id, title, thumbnail_url, embedding
            FROM content
            """
      cursor.execute(sql)
      rows = cursor.fetchall()
      return { row['id']: {
                  'title': row['title'],
                  'embedding': json.loads(row['embedding']),
                  'thumbnail_url': row['thumbnail_url'],
                } for row in rows
              }
    
def init_vector():

  with get_connection() as conn:
    with conn.cursor() as cursor:
      sql = """
            SELECT
              mic.content_id,
              mi.name AS genre_name
            FROM
              meta_info_contents mic
            JOIN
              meta_info mi ON mic.meta_info_id = mi.id
            WHERE
              mi.type = 'GENRE'
            ORDER BY
              mic.content_id
            """
      cursor.execute(sql)
      rows = cursor.fetchall()
      print(rows)
  content_genre_map = defaultdict(list)
  for item in rows:
    content_id = item['content_id']
    genre = item['genre_name']
    content_genre_map[content_id].append(genre)

  with open("insert_embeddings.sql", "w", encoding="utf-8") as f:
    for content_id, genres in content_genre_map.items():
      print(f'{content_id} : {genres}')
      genre_vectors = []
      for genre in genres:
        model_genre = db_w2v_mapper.translate_genre(genre)
        genre_vectors.append(word2vec_util.get_vector(model_genre))
      content_vec = np.mean(genre_vectors, axis=0)

      embedding_str = str(content_vec.tolist())
      sql = f"UPDATE contents SET embedding = '{embedding_str}' WHERE id = {content_id};\n"
      f.write(sql)
