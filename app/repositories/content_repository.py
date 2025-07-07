import json
from app.db import get_connection

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
