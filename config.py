import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FFmpeg configuration
# Provide paths via environment or fallback to defaults
FFMPEG_BINARY = os.getenv("FFMPEG_BINARY", r"C:\Users\Pc\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe")
FFPROBE_BINARY = os.getenv("FFPROBE_BINARY", r"C:\Users\Pc\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe")
FFMPEG_PATH = os.getenv("FFMPEG_PATH", r"C:\Users\Pc\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin")

# Set binaries in environment
os.environ["FFMPEG_BINARY"] = FFMPEG_BINARY
os.environ["FFPROBE_BINARY"] = FFPROBE_BINARY
# Extend PATH for ffmpeg tools
os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# AWS & Gemini keys
GEMINI_API_KEY   = os.getenv('GEMINI_API_KEY')
AWS_ACCESS_KEY   = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY   = os.getenv('AWS_SECRET_KEY')
AWS_REGION       = os.getenv('AWS_REGION', "us-east-1")

# Upload and music directories (configurable via env)
UPLOAD_FOLDER    = os.getenv("UPLOAD_FOLDER", "uploads")
MUSIC_FOLDER     = os.getenv(
    "MUSIC_FOLDER",
    r"C:\Users\Pc\OneDrive\Desktop\Directory\College-CCE\Projects\Extras\Delta\Musics\Military"
)

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)

# Validate required settings
_missing = []
for name in ("GEMINI_API_KEY", "AWS_ACCESS_KEY", "AWS_SECRET_KEY"):
    if not globals().get(name):
        _missing.append(name)
if _missing:
    raise RuntimeError(f"Missing required config variables: {', '.join(_missing)}")
