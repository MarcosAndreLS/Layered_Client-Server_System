"""Servidor flask"""
from flask import Flask
from config import Config
from database.db import init_db
from routes.images import get_image, get_images
from routes.api import upload_file

app = Flask(__name__)
app.config.from_object(Config)

# Inicialização
Config.init_folders()
init_db()

# Rotas
app.add_url_rule('/upload', 'upload_file', upload_file, methods=['POST'])
app.add_url_rule('/image/<path:filename>', 'get_image', get_image)
app.add_url_rule('/images', 'get_images', get_images, methods=['GET'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)