from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import base64

# Initialize the Flask app
main = Flask(__name__, static_folder='styles', template_folder='interface')


# Directory to store captured images  
IMAGE_DIR = os.path.join(main.static_folder, 'images')
os.makedirs(IMAGE_DIR, exist_ok=True) # Ensure the directory exists


@main.route('/')
def index():
    # Render the camera page
    return render_template('camera.html')

@main.route('/gallery')
def gallery():
    # Render the gallery page
    return render_template('gallery.html')

@main.route('/save-image', methods=['POST'])
def save_image():
    # Handle saving of images from the camera
    data = request.json
    image_data = data.get('image')
    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    # Decode the base64 image
    image_bytes = base64.b64decode(image_data.split(',')[1])
    filename = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(IMAGE_DIR, filename)

    # Save the image
    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    return jsonify({'message': 'Image saved successfully', 'filename': filename})

@main.route('/images')
def get_images():
    # Fetch all images in the images directory
    image_files = [
        {
            "name": f,
            "path": f"/styles/images/{f}"
        }
        for f in os.listdir(IMAGE_DIR) if f.endswith(('png', 'jpg', 'jpeg'))
    ]
    return jsonify(image_files)

@main.route('/image-details/<filename>')
def image_details(filename):
    # Get details of a specific image
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)  # Size in bytes
        file_time = os.path.getmtime(file_path)  # Modification time
        formatted_time = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({
            "name": filename,
            "size": f"{file_size / 1024:.2f} KB",
            "time": formatted_time
        })
    return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    # Run the Flask app
    main.run(debug=True)
