from flask import Flask, render_template, request
from PIL import Image
import random
import os

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

    # Create output folder if it doesn't exist
    output_folder = "output_folder"
    os.makedirs(output_folder, exist_ok=True)

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

    return "Watermarking complete."

if __name__ == '__main__':
    # Get the port from the environment variable, or use 8080 as a default
    port = int(os.environ.get('PORT', 8080))
    # Start the app with binding to 0.0.0.0 to allow external connections
    app.run(host='0.0.0.0', port=port)
