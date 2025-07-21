from typing import List
import asyncpg

async def get_genre_id_by_content_id(content_id: int) -> List[str]:
    conn = await asyncpg.connect(
        user='your_user',
        password='your_password',
        database='your_db',
        host='your_host',  # 예: 'localhost' 또는 RDS 주소
        port=5432
    )

    query = """
    SELECT DISTINCT mi.name
    FROM meta_info_contents mic
    JOIN meta_info mi ON mic.meta_info_id = mi.id
    WHERE mic.content_id = $1
    """

    rows = await conn.fetch(query, content_id)
    await conn.close()

    return [row["name"] for row in rows]