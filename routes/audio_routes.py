import io, os
import glob
import random
from flask import Blueprint, request, jsonify, current_app, send_file
from utils.genai_utils import extract_and_summarize
from utils.aws_utils import synthesize_speech
from pydub import AudioSegment

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    image_id = data.get('imageId')
    voice = data.get('voice', 'Matthew')
    add_bgm = data.get('addBackgroundMusic', True)

    if not image_id:
        return jsonify({'success': False, 'message': 'No image ID provided'})

    uploads = current_app.config['UPLOAD_FOLDER']
    music_dir = current_app.config.get('MUSIC_FOLDER', None)
    
    # Use os.path.join for proper path construction
    image_path = os.path.join(uploads, image_id)
    raw_path = os.path.join(uploads, f"{image_id.split('.')[0]}_raw.mp3")
    final_path = os.path.join(uploads, f"{image_id.split('.')[0]}.mp3")

    try:
        print(f"DEBUG: Extracting text from image: {image_path}")
        extracted = extract_and_summarize(image_path)
        print(f"DEBUG: Extracted text: {extracted[:100]}...")
        
        print(f"DEBUG: Synthesizing speech with voice: {voice}")
        synth_resp = synthesize_speech(text=extracted, voice=voice)
        print(f"DEBUG: Speech synthesis response size: {len(synth_resp)} bytes")
        
        with open(raw_path, 'wb') as f:
            f.write(synth_resp)
        print(f"DEBUG: Raw audio saved to: {raw_path}")

        # Check if raw file was actually created
        if not os.path.exists(raw_path):
            raise Exception(f"Raw audio file was not created: {raw_path}")

        print(f"DEBUG: add_bgm={add_bgm}, music_dir={music_dir}")
        
        if add_bgm and music_dir and os.path.exists(music_dir):
            bg_files = glob.glob(os.path.join(music_dir, "*.mp3"))
            print(f"DEBUG: Background music files found: {len(bg_files)}")
            
            if bg_files:
                print("DEBUG: Adding background music")
                bg = AudioSegment.from_mp3(random.choice(bg_files)).apply_gain(-21)
                speech = AudioSegment.from_mp3(raw_path)
                if speech.frame_rate != bg.frame_rate:
                    bg = bg.set_frame_rate(speech.frame_rate)
                bg = (bg * ((len(speech)//len(bg))+1))[:len(speech)]
                combo = speech.overlay(bg)
                combo.export(final_path, format='mp3')
                print(f"DEBUG: Final audio with BGM saved to: {final_path}")
            else:
                print("DEBUG: No background music files found, copying raw audio")
                AudioSegment.from_mp3(raw_path).export(final_path, format='mp3')
                print(f"DEBUG: Final audio (no BGM) saved to: {final_path}")
        else:
            print("DEBUG: Background music disabled or directory not found, copying raw audio")
            AudioSegment.from_mp3(raw_path).export(final_path, format='mp3')
            print(f"DEBUG: Final audio (no BGM) saved to: {final_path}")

        # Verify final file was created
        if not os.path.exists(final_path):
            raise Exception(f"Final audio file was not created: {final_path}")
        
        print(f"DEBUG: Final file size: {os.path.getsize(final_path)} bytes")

        return jsonify({
            'success': True,
            'audioUrl': f"/api/audio/{image_id.split('.')[0]}.mp3",
            'extractedText': extracted,
            'message': 'Audio generated successfully'
        })
    except Exception as e:
        print(f"ERROR in generate_audio: {e}")
        return jsonify({'success': False, 'message': f"Error: {e}"})


@audio_bp.route('/api/audio/<filename>')
def serve_audio(filename):
    try:
        uploads_folder = current_app.config['UPLOAD_FOLDER']
        
        # Ensure we have the absolute path
        uploads_folder = os.path.abspath(uploads_folder)
        
        # Remove .mp3 extension to get base filename
        base_filename = filename.replace('.mp3', '')
        
        # Try these files in order of preference with proper path joining
        possible_files = [
            os.path.join(uploads_folder, f'{base_filename}.mp3'),      # Final processed file
            os.path.join(uploads_folder, f'{base_filename}_raw.mp3'),  # Raw file as backup
        ]
        
        print(f"DEBUG: Looking for audio file with base name: {base_filename}")
        print(f"DEBUG: Uploads folder: {uploads_folder}")
        print(f"DEBUG: Possible files: {possible_files}")
        
        for file_path in possible_files:
            print(f"DEBUG: Checking if exists: {file_path}")
            if os.path.exists(file_path):
                print(f"DEBUG: Found and serving: {file_path}")
                return send_file(file_path, mimetype='audio/mpeg', as_attachment=False)
        
        # If no files found, list what's actually in the uploads folder
        if os.path.exists(uploads_folder):
            actual_files = os.listdir(uploads_folder)
            matching_files = [f for f in actual_files if base_filename in f and f.endswith('.mp3')]
            print(f"DEBUG: No exact match found. Base filename: {base_filename}")
            print(f"DEBUG: Files in uploads folder: {actual_files}")
            print(f"DEBUG: Matching files: {matching_files}")
            
            # If there are matching files, serve the first one
            if matching_files:
                file_path = os.path.join(uploads_folder, matching_files[0])
                print(f"DEBUG: Serving closest match: {file_path}")
                return send_file(file_path, mimetype='audio/mpeg', as_attachment=False)
        
        print(f"ERROR: Audio file not found - {filename}")
        return "Audio file not found", 404
            
    except Exception as e:
        print(f"ERROR serving audio: {e}")
        import traceback
        traceback.print_exc()
        return "Error serving audio file", 500