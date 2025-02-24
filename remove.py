# Biblioteca que permite utilizar as funcionalidades do sistema operacional
import os

# Caminho da pasta que terá os arquivos renomeados
folder = r"Z:\Almoxarifado\01-Imagens e Vídeos\2014\20-05-2014"
# Entra no diretório descrito acima
os.chdir(folder)

# Laço que vai percorrer todos os arquivos dentro da pasta
for file_name in os.listdir():
  # Separa o nome do arquivo da extensão
  f_name, f_ext = (os.path.splitext(file_name))
  if (len(f_name.split(" ")) > 1):
    os.remove(file_name)