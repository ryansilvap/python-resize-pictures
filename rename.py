import os, shutil, PIL
from PIL import Image

folder = r'C:\Users\ryan.pereira\Desktop\Imagens'

count = 0

for path, directories, files in os.walk(folder):
  print(
    f'\npath: {path}\n'
    f'directories: {directories}\n'
    f'files: {files}'
  )

  for file in files:
    full_name, extension = os.path.splitext(file)
    new_name = f'{full_name} (Large){extension}'
    if extension.lower() == '.jpg':
      if int(os.path.getsize(f'{path}/{file}')) > 700000 and file != 'Thumbs.db':

        #resizing images
        image_width = 1440
        image_height = 1080

        with Image.open(os.path.join(path, file)) as image:
          image = image.resize((image_width, image_height), PIL.Image.NEAREST)
          image.save(os.path.join(path, new_name))
          shutil.copystat(os.path.join(path, file), os.path.join(path, new_name))

        #renaming files
        if len(full_name.split(' ')) == 2:
          first_name, second_name = full_name.split(' ')
          first_name = first_name.strip()
          os.rename(os.path.join(path, file), os.path.join(path, f'{first_name}{extension}'))
          count += 1

print(f'\nItens processados: {count}')
