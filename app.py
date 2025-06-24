import os
# from fpdf import FPDF
from ResizePicture import resize_picture
from Remove import remove_original_file
from Rename import rename_resized_file

folder = r'C:\Users\ryan.pereira\Desktop\Imagens'
count = 0

# First loop: Resize images and remove originals
for path, directories, files in os.walk(folder):
    if files:
        # pdf = FPDF()
        # pdf.add_page()
        # pdf.set_font('Arial', 'B', 12)
        # pdf.cell(40, 10, f'{path}', 0)
        # pdf.ln(10)

        for file in files:
            name, extension = os.path.splitext(file)
            new_name = f'{name} (Large){extension}'
            file_path = os.path.join(path, file)

            if extension.lower() == '.jpg' or extension.lower() == '.jpeg' and file != 'Thumbs.db':
                if os.path.exists(file_path) and os.path.getsize(file_path) > 2000 * 1024:
                    resize_picture(path, file, new_name)
                    remove_original_file(path, file)
                    count += 1

       # pdf.output(os.path.join(path,'report.pdf'))

# Second loop: Rename resized files back to original name
for path, directories, files in os.walk(folder):
    for file in files:
        name, extension = os.path.splitext(file)
        if "(Large)" in name:
            rename_resized_file(path, file, name, extension)

print(f'\nItems processed: {count}')
