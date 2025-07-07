from app.db import get_connection
from app.error.user_not_found_error import UserNotFoundError
from app.error.weight_not_found_error import WeightNotFoundError

def user_weight(user_id: int) -> dict[str, float]:
  with get_connection() as conn:
    with conn.cursor() as cursor:
      user_id = find_user_by_id(user_id)
      sql = """
            SELECT m.name, p.weight
            FROM prefer_meta_info p JOIN meta_info m ON p.meta_info_id = m.id
            WHERE p.user_id = %s
            """
      cursor.execute(sql, (user_id,))
      rows = cursor.fetchall()

      if not rows:
        raise WeightNotFoundError(user_id)
      
      return {row['name']: row['weight'] for row in rows}

def find_user_by_id(user_id: int) -> int:
  with get_connection() as conn:
    with conn.cursor() as cursor:
      sql = """
            SELECT id FROM users
            WHERE id = %s
            """
      cursor.execute(sql, (user_id,))
      row = cursor.fetchone()

      if not row:
        raise UserNotFoundError(user_id)
      
      return row['id']
