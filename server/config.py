import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed'
    DATABASE = 'database/images.db'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    API_KEY = 'SECRET_KEY_123'
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8MB

    @staticmethod
    def init_folders():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)