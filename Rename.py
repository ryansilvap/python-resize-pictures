import os, re

def rename_resized_file (path, file, name, extension):
  """Rename the resized file back to its original name."""
  file_path = os.path.join(path, file)

  match = re.match(r'^(.*?)\s*\(Large\)$', name)
  if match:
    basename = match.group(1).strip()
    new_name = f'{basename}{extension}'
    renamed_path = os.path.join(path, new_name)

    if os.path.exists(renamed_path):
      print(f'Skipping rename: {renamed_path} already exists!')
    else:
      os.rename(file_path, renamed_path)
      print(f' Renamed {file} -> {new_name}')