import shutil

import PIL, os
from PIL import Image

file = r'C:\Users\ryan.pereira\Desktop\Imagens\Almoxarifado\01 - Imagens e Vídeos\2016\04-04-2016\DSC01731.JPG'
name, extension = os.path.splitext(file)
new_file = f'{name} (Large){extension}'

with Image.open(file) as my_image:
    image_height = 1080
    image_width = 1440

    print('Size of image is: ', round(len(my_image.fp.read())/1024),'KB')

    # my_image = my_image.resize((image_width, image_height),PIL.Image.NEAREST)
    my_image = my_image.resize((image_width, image_height), PIL.Image.NEAREST)

    my_image.save(new_file)

shutil.copystat(file, new_file)

with Image.open(r'C:\Users\ryan.pereira\Desktop\Imagens\Almoxarifado\01 - Imagens e Vídeos\2016\04-04-2016\DSC01731 (Large).JPG') as new_image:
    print('Size of new image is: ', round(len(new_image.fp.read())/1024),'KB')
