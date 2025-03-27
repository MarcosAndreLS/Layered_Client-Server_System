import os
from config import ClientConfig

def ensure_processed_folder():
    os.makedirs(ClientConfig.PROCESSED_FOLDER, exist_ok=True)

def get_processed_filename(original_path, filter_type):
    original_name = os.path.basename(original_path)
    name, ext = os.path.splitext(original_name)
    return f"{name}_{filter_type}{ext}"

def save_processed_image(content, filename):
    filepath = os.path.join(ClientConfig.PROCESSED_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(content)
    return filepath