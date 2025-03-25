"""Servidor flask
"""
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = '../images/uploads'
PROCESSED_FOLDER = '../images/processed'
DATABASE = 'images.db'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Inicialização do banco de dados
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  filter_type TEXT,
                  original_path TEXT,
                  processed_path TEXT,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

def apply_filter(image, filter_type):
    """Aplica filtro na imagem conforme solicitado"""
    if filter_type == 'pixelate':
        # Pixelização reduzindo e ampliando a imagem
        small = image.resize((32, 32), resample=Image.BILINEAR)
        return small.resize(image.size, Image.NEAREST)
    elif filter_type == 'grayscale':
        return image.convert('L')
    elif filter_type == 'blur':
        return image.filter(ImageFilter.BLUR)
    elif filter_type == 'invert':
        return Image.eval(image, lambda x: 255 - x)
    else:
        return image  # Sem filtro

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    filter_type = request.form.get('filter', 'pixelate')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Salva a imagem original
        original_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(original_path)
        
        # Abre a imagem e aplica o filtro
        img = Image.open(original_path)
        processed_img = apply_filter(img, filter_type)
        
        # Salva a imagem processada
        processed_filename = f"processed_{file.filename}"
        processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
        processed_img.save(processed_path)
        
        # Salva metadados no banco de dados
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO images (filename, filter_type, original_path, processed_path, created_at) VALUES (?, ?, ?, ?, ?)",
                  (file.filename, filter_type, original_path, processed_path, datetime.now()))
        conn.commit()
        conn.close()
        
        return jsonify({
            'original': original_path,
            'processed': processed_path,
            'filter': filter_type
        })

@app.route('/image/<path:filename>')
def get_image(filename):
    return send_file(filename)

@app.route('/images')
def get_images():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM images ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)