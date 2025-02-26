import os, re

folder =  r'C:\Users\ryan.pereira\Desktop\Imagens'
count = 0

for path, directories, files in os.walk(folder):
  print(
    f'\npath: {path}'
    f'\ndirectory: {directories}'
    f'\nfiles: {files}'
  )

  for file in files:
    name, extension = os.path.splitext(file)

    if re.search('(Large)', name):
      os.remove(os.path.join(path, file))
      print(f'File {file} removed')
      count += 1
print(f'Total: {count}')