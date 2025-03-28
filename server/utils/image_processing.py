from PIL import Image, ImageFilter

def apply_filter(image, filter_type):
    """Aplica filtro na imagem"""
    if filter_type == 'pixelate':
        small = image.resize((32, 32), resample=Image.BILINEAR)
        return small.resize(image.size, Image.NEAREST)
    elif filter_type == 'grayscale':
        return image.convert('L')
    elif filter_type == 'blur':
        return image.filter(ImageFilter.BLUR)
    elif filter_type == 'invert':
        return Image.eval(image, lambda x: 255 - x)
    return image