from flask import send_file, jsonify, request
from utils.auth import auth_required
from database.models import Image
from datetime import datetime

@auth_required
def get_image(filename):
    try:
        return send_file(filename)
    except FileNotFoundError:
        return jsonify({'error': 'Imagem não encontrada'}), 404

@auth_required
def get_images():
    rows = Image.get_all()
    images = []
    for row in rows:
        images.append({
            'id': row[0],
            'filename': row[1],
            'filter': row[2],
            'original_path': row[3],
            'processed_path': row[4],
            'created_at': row[5]
        })
    return jsonify(images)