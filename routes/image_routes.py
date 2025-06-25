import uuid
from flask import Blueprint, request, jsonify, current_app
import cv2
from PIL import Image
import io
from utils.image_utils import process_image_array

image_bp = Blueprint('image', __name__)

@image_bp.route('/api/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file provided'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if not file.content_type.startswith('image/'):
        return jsonify({'success': False, 'message': 'Invalid file type'})

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = f"{current_app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(filepath)

    try:
        denoised = process_image_array(filepath)
        Image.fromarray(denoised).save(filepath)
        return jsonify({'success': True, 'imageId': filename, 'message': 'Image processed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Error: {e}"})
