from app.db import get_connection
from app.exceptions.user_not_found_execption import UserNotFoundException

def user_weight(user_id: str) -> dict[str, float]:
  with get_connection() as conn:
    with conn.cursor() as cursor:
      sql = """
            SELECT m.name, p.weight
            FROM prefer_meta_info p JOIN meta_info m ON p.meta_info_id = m.id
            WHERE p.user_id = %s
            """
      cursor.execute(sql, (user_id,))
      rows = cursor.fetchall()

      if not rows:
        raise UserNotFoundException(user_id)
      
      return {row['name']: row['weight'] for row in rows}
