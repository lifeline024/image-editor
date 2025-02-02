from flask import Flask, render_template, request, send_file
from PIL import Image, ImageEnhance, ImageFilter
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp for temporary file storage in Vercel
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route to display the upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and processing
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    action = request.form.get('action')

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        img = Image.open(filepath)

        # Apply selected filters
        if action == 'grayscale':
            img = img.convert('L')
        elif action == 'blur':
            img = img.filter(ImageFilter.BLUR)
        elif action == 'sharpen':
            img = img.filter(ImageFilter.SHARPEN)
        elif action == 'edge_enhance':
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif action == 'sepia':
            sepia_img = img.convert("RGB")
            width, height = sepia_img.size
            pixels = sepia_img.load()

            for py in range(height):
                for px in range(width):
                    r, g, b = sepia_img.getpixel((px, py))
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))

            img = sepia_img
        elif action == 'invert':
            img = Image.eval(img, lambda x: 255 - x)
        elif action == 'rotate':
            img = img.rotate(90)
        elif action == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.5)  # Increase brightness
        elif action == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)  # Increase contrast
        elif action == 'resize':
            img = img.resize((400, 400))

        edited_path = os.path.join(app.config['UPLOAD_FOLDER'], f"edited_{file.filename}")
        img.save(edited_path)

        return send_file(edited_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
