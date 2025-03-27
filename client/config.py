class ClientConfig:
    SERVER_URL = "http://127.0.0.1:5000"
    API_KEY = "SECRET_KEY_123"
    PROCESSED_FOLDER = "processed_images"
    ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp')
    MAX_IMAGE_SIZE = (400, 400)  # Para visualização
    TIMEOUT = 5  # segundos para requisições