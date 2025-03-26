import os

def remove_original_file (path, file):
  """Remove the original file after resizing."""
  file_path = os.path.join(path, file)

  if os.path.exists(file_path):
    os.remove(file_path)
    print(f'Removed original: {file}')