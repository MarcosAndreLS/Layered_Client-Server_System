"""Servidor flask
"""
from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
DATABASE = 'images.db'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
API_KEY = 'SECRET_KEY_123'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f'Bearer {API_KEY}':
        return False
    return True

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
    if not authenticate():
        return jsonify({"error": "Sem autorização"}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'Nenhuma parte do arquivo'}), 400
    
    file = request.files['file']
    filter_type = request.form.get('filter', 'pixelate')
    
    if file.filename == '':
        return jsonify({'error': 'Arquivo não selecionado'}), 400
    
    if file and allowed_file(file.filename):
        # Salva a imagem original
        filename = secure_filename(file.filename)
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(original_path)
        
        # Abre a imagem e aplica o filtro
        try:
            img = Image.open(original_path)
            processed_img = apply_filter(img, filter_type)
            
            # Salva a imagem processada
            processed_filename = f"processed_{filename}"
            processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            processed_img.save(processed_path)
            
            # Salva metadados no banco de dados
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("INSERT INTO images (filename, filter_type, original_path, processed_path, created_at) VALUES (?, ?, ?, ?, ?)",
                    (filename, filter_type, original_path, processed_path, datetime.now()))
            conn.commit()
            conn.close()
            
            return jsonify({
                'status': 'success',
                'original': f"/image/{original_path}",
                'processed': f"/image/{processed_path}",
                'filter': filter_type
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

@app.route('/image/<path:filename>')
def get_image(filename):
    if not authenticate():
        return jsonify({'error': 'Não autorizado'})
    
    try:
        return send_file(filename)
    except FileNotFoundError:
        return jsonify({'error': 'Imagem não encontrada'})

@app.route('/images')
def get_images():
    if not authenticate():
        return jsonify({'error': 'Não autorizado'})
    
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
    app.run(host='26.212.178.226',debug=True, port=5000)