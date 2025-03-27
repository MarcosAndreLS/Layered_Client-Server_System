from flask import request, jsonify
from config import Config

def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f'Bearer {Config.API_KEY}':
        return False
    return True

def auth_required(f):
    def wrapper(*args, **kwargs):
        if not authenticate():
            return jsonify({"error": "Sem autorização"}), 401
        return f(*args, **kwargs)
    return wrapper