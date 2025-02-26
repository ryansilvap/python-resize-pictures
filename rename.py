import os, re, shutil, PIL
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
    name, extension = os.path.splitext(file)
    new_name = f'{name} (Large){extension}'
    if extension.lower() == '.jpg':
      if int(os.path.getsize(f'{path}/{file}')) > 700000 and file != 'Thumbs.db':

        #resizing images
        with Image.open(os.path.join(path, file)) as image:
          image_width = image.width
          image_height = image.height

          image = image.resize((image_width, image_height), PIL.Image.NEAREST)
          image.save(os.path.join(path, new_name))
          shutil.copystat(os.path.join(path, file), os.path.join(path, new_name))

        #removing files
        if re.search('(Large)', name):
          os.remove(os.path.join(path, file))
          print(f'File {file} removed')
          count += 1

        #renaming files
        if re.search('(Large)', new_name):
          first_name, large = name.split(' (Large)')
          first_name = first_name.strip()
          os.rename(os.path.join(path, file), os.path.join(path, f'{first_name}{extension}'))
          count += 1

print(f'\nItens processados: {count}')
