import os, PIL, shutil
from PIL import Image

def resize_picture (path, file, new_name):
    """Resize an image and copy timestamps."""
    file_path = os.path.join(path, file) # Full path of original image
    new_file_path = os.path.join(path, new_name) # Full path for resized image

    with Image.open(file_path) as image:
        image_width = image.width
        image_height = image.height

        image_resized = image.resize((image_width, image_height), PIL.Image.NEARSET)
        image_resized.save(new_file_path)
        shutil.copystat(file_path, new_file_path)
        print(f'Resized: {file} -> {new_name}')