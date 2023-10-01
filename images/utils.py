
import os
from PIL import Image as PillowImage
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


def resize_image(image_obj, size):
    """
    Returns resized image
    """
    # Image path
    sc_dir = os.path.dirname(os.path.abspath(__file__))
    img_name = image_obj.image.url.replace('/', '\\')
    absolute_path = sc_dir[0:-7] + '\\' +  img_name
    img_path = absolute_path
    # Open image with Pillow
    img = PillowImage.open(img_path)
    # Define new size
    new_size = (size, size)
    # Resize image
    img.thumbnail(new_size)
    # Save resized image to memory
    io = BytesIO()
    img.save(io, img.format)
    io.seek(0)
    # Return created file object
    return SimpleUploadedFile('image.jpg', io.read(), content_type='image/jpeg')
