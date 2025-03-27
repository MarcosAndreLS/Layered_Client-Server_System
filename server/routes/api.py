from flask import request, jsonify
from PIL import Image as PILImage
from utils.auth import auth_required
from utils.file_handling import allowed_file, secure_save
from utils.image_processing import apply_filter
from database.models import Image
from config import Config
import os

@auth_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhuma parte do arquivo'}), 400
    
    file = request.files['file']
    filter_type = request.form.get('filter', 'pixelate')
    
    if file.filename == '':
        return jsonify({'error': 'Arquivo não selecionado'}), 400
    
    if not (file and allowed_file(file.filename)):
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

    try:
        # Salva a imagem original
        original_path, filename = secure_save(file, Config.UPLOAD_FOLDER)
        name, ext = os.path.splitext(filename)
        
        # Processa a imagem
        img = PILImage.open(original_path)
        processed_img = apply_filter(img, filter_type)
        
        # Salva a imagem processada
        processed_filename = f"{name}_{filter_type}{ext}"
        processed_path = os.path.join(Config.PROCESSED_FOLDER, processed_filename)
        processed_img.save(processed_path)
        
        # Salva no banco de dados
        Image.create(filename, filter_type, original_path, processed_path)
        
        return jsonify({
            'status': 'success',
            'original': f"/image/{original_path}",
            'processed': f"/image/{processed_path}",
            'filter': filter_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500