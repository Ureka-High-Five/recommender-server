import pymysql
from app.settings import settings

def get_connection():
  return pymysql.connect(
    host=settings.DB_HOST,
    user=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
  )