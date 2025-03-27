from datetime import datetime
from database.db import get_db_connection

class Image:
    @staticmethod
    def create(filename, filter_type, original_path, processed_path):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO images (filename, filter_type, original_path, processed_path, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (filename, filter_type, original_path, processed_path, datetime.now())
        )
        conn.commit()
        conn.close()
        return cursor.lastrowid

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows