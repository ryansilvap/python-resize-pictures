import os, PIL, shutil, jinja2, pdfkit
from PIL import Image
from datetime import datetime

def resize_picture (path, file, new_name):
    """Resize an image and copy timestamps."""
    file_path = os.path.join(path, file) # Full path of original image
    new_file_path = os.path.join(path, new_name) # Full path for resized image
    date = datetime.today().strftime("%d %b, %Y")

    with Image.open(file_path) as image:
        image_width = image.width
        image_height = image.height

        image_resized = image.resize((image_width, image_height), PIL.Image.NEAREST)
        image_resized.save(new_file_path)
        shutil.copystat(file_path, new_file_path)

        original_size = os.path.getsize(file_path) / 1024 / 1024
        resized_size = os.path.getsize(new_file_path) / 1024 / 1024
        difference = round((resized_size / original_size) * 100 ,2)

        context = {"path": path, "date": date, "file": file, "new_name": new_name, "difference": difference}

        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template("template.html")
        output_text = template.render(context)

        config = pdfkit.configuration(wkhtmltopdf=r"C:\wkhtmltox\bin/wkhtmltopdf.exe")
        pdfkit.from_string(output_text, os.path.join(path,'report_pdfkit.pdf'), configuration=config)

        # pdf.cell(40, 10, f'Resized: {file} {round(original_size, 2)} MB | Resized: {new_name} {round(resized_size, 2)} MB | % Difference: {round(difference, 2)}%', 0)
        # pdf.ln(4)

        # print(f'\nResized: {file} {round(original_size, 2)} MB | Resized: {new_name} {round(resized_size, 2)} MB | % Difference: {round(difference, 2)}%')

        # if not r'C:\Users\ryan.pereira\Desktop\report.txt':
        #     with open(r'C:\Users\ryan.pereira\Desktop\report.txt', 'w') as report:
        #         report.write(f'Resized: {file} -> {new_name}')
        # else:
        #     with open(r'C:\Users\ryan.pereira\Desktop\report.txt', 'a') as report:
        #         report.write(f'\nResized: {file} {round(os.path.getsize(file_path) / 1024 / 1024, 2)} mb -> {new_name} {round(os.path.getsize(new_file_path) / 1024 / 1024, 2)} mb')