from flask import Flask, render_template, request, send_file
from PIL import Image
import random
import os
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    watermark_scale = float(request.form['watermark_scale'])
    watermark_x = int(request.form['watermark_x'])
    watermark_y = int(request.form['watermark_y'])

    image_files = request.files.getlist("image")
    watermark_files = request.files.getlist("watermarks")
    download_format = request.form['download_format']  # New field for download format
    
    # Create output folder if it doesn't exist
    output_folder = "output_folder"
    os.makedirs(output_folder, exist_ok=True)

    processed_images = []

    while image_files:
        selected_image = image_files.pop()
        img = Image.open(selected_image)

        # Randomly select a watermark for each image
        selected_watermark = Image.open(random.choice(watermark_files))
        watermark_resized = selected_watermark.resize(
            (int(selected_watermark.width * watermark_scale), int(selected_watermark.height * watermark_scale))
        )

        watermarked_img = img.copy()
        watermarked_img.paste(watermark_resized, (watermark_x, watermark_y), watermark_resized)

        output_path = os.path.join(output_folder, f"watermarked_{selected_image.filename}")
        watermarked_img.save(output_path)
        processed_images.append(output_path)

    # Create a zip file containing the processed images
    zip_filename = 'processed_images.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for image_path in processed_images:
            zipf.write(image_path, os.path.basename(image_path))
            os.remove(image_path)  # Remove the individual processed images

    # Remove the output folder
    os.rmdir(output_folder)

    # Send the zip file for download
    if download_format == 'zip':
        return send_file(zip_filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
