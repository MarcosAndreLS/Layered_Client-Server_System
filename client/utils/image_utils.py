from PIL import Image, ImageTk
from io import BytesIO
from config import ClientConfig

def open_image(file_path):
    return Image.open(file_path)

def resize_image(img, max_size=ClientConfig.MAX_IMAGE_SIZE):
    img_copy = img.copy()
    img_copy.thumbnail(max_size)
    return img_copy

def image_to_tk(img):
    return ImageTk.PhotoImage(img)

def bytes_to_image(image_bytes):
    return Image.open(BytesIO(image_bytes))