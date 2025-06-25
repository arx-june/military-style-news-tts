from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import glob
import os

music_bp = Blueprint('music', __name__)

@music_bp.route('/api/upload-background-music', methods=['POST'])
def upload_music():
    if 'music' not in request.files:
        return jsonify({'success': False, 'message': 'No music file provided'})
    file = request.files['music']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})

    filename = secure_filename(file.filename)
    if not filename.endswith('.mp3'):
        filename += '.mp3'
    
    if not file.content_type.startswith('audio/'):
        return jsonify({'success': False, 'message': 'Invalid file type'})

    path = os.path.join(current_app.config['MUSIC_FOLDER'], filename)
    file.save(path)
    return jsonify({'success': True, 'message': 'Background music uploaded successfully'})

@music_bp.route('/api/list-background-music', methods=['GET'])
def list_music():
    music_dir = current_app.config['MUSIC_FOLDER']
    bg_files = glob.glob(f"{music_dir}/*.mp3")
    music_list = [os.path.basename(f) for f in bg_files]
    return jsonify({'success': True, 'music_files': music_list})
