import sqlite3
from config import Config

def get_db_connection():
    return sqlite3.connect(Config.DATABASE)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS images
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      filename TEXT,
                      filter_type TEXT,
                      original_path TEXT,
                      processed_path TEXT,
                      created_at TIMESTAMP)''')
    conn.commit()
    conn.close()