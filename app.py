from flask import Flask, render_template
from config import UPLOAD_FOLDER, MUSIC_FOLDER
from routes.image_routes import image_bp
from routes.audio_routes import audio_bp
from routes.music_routes import music_bp
import google.generativeai as genai
import config, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MUSIC_FOLDER'] = MUSIC_FOLDER

    # Configure Gemini API
    genai.configure(api_key=config.GEMINI_API_KEY)

    # Register blueprints
    app.register_blueprint(image_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(music_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
