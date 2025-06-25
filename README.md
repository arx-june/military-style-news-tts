# 🪖 WarCast AI — AI-Powered Military-Style News Summarizer & Audio Briefing Generator

> An end-to-end app that transforms news article **images** into summarized **audio briefings** with military-style **background music**, using LLMs, Amazon Polly, and FFmpeg. All hosted on a slick Flask frontend.

---

## 📸 What It Does

1. 🖼️ The User uploads a **news article image** (screenshot/photo)
2. 🤖 Application Extracts text using **Gemini 2.5 Flash** (OCR + Summarization)
3. 🎤 Converts summary to **voice** using **Amazon Polly**
4. 🥁 Mixes it with **military-themed background music**
5. 🎧 Lets you play/download the final audio — all in the browser

---

## 🧠 Tech Stack

| Layer        | Tools Used                                                                 |
|--------------|------------------------------------------------------------------------------|
| Frontend     | HTML, CSS, JS (vanilla)                                                    |
| Backend      | Python (Flask)                                                              |
| OCR + LLM    | Gemini 2.5 Flash                                                            |
| TTS          | Amazon Polly                                                                |
| Audio Mixing | `ffmpeg`                                                                    |
| Secrets Mgmt | `dotenv`                                                                    |

---

## 🖥️ Project Structure

```
Delta/
├── app.py                  # Main Flask app
├── config.py               # Loads all keys & settings
├── requirements.txt        # All dependencies
│
├── templates/
│   └── index.html          # Web UI
│
├── static/                 # CSS, JS, Logo
├── routes/                 # Flask API routes (audio, image, music)
├── utils/                  # Helper functions (AWS, LLM, image)
├── Musics/Military/        # Background tracks
├── uploads/                # Temporary upload storage
└── .env                    # Secrets (NOT pushed)
```

---

## 🚀 Getting Started (for Newbies)

### 1. 🔁 Clone this repo
```bash
git clone https://github.com/arx-june/military-style-news-tts.git
cd military-style-news-tts
```

### 2. 🐍 Create & activate a virtual environment (recommended)
```bash
# For Windows:
python -m venv venv
venv\Scripts\activate

# For Mac/Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### 4. 🔐 Create a `.env` file in the root folder
Example:
```dotenv
AWS_ACCESS_KEY=your_access_key_here
AWS_SECRET_KEY=your_secret_key_here
AWS_REGION=us-east-1
GEMINI_API_KEY=your_gemini_key_here

FFMPEG_BINARY=C:\path\to\ffmpeg.exe
FFPROBE_BINARY=C:\path\to\ffprobe.exe
FFMPEG_PATH=C:\path\to\ffmpeg-folder
```

### 5. ▶️ Run the app
```bash
python app.py
```
Open your browser and go to: [http://localhost:5000](http://localhost:5000)

---

## 🛡️ Features
- ✅ Gemini-based OCR + summarization
- ✅ Amazon Polly-based voice synthesis
- ✅ Military-themed background music
- ✅ Audio mixing via FFmpeg
- ✅ Simple UI with upload + playback

---

## 🔐 Security Notes
- `.env` is used to store credentials and should **never be pushed** to GitHub.
- `config.py` reads all secrets from the environment.

---

## 📤 To-Do / Future Enhancements
- [ ] Multi-language support (regional + English)
- [ ] Upload via URL (news screenshot links)
- [ ] Daily Telegram/WhatsApp briefings
- [ ] React frontend rewrite for better UX
- [ ] Auto-deletion of old audio + uploads

---

## 👨‍💻 Authors
- **Arjun Manoj**    
🔗 [LinkedIn](https://www.linkedin.com/in/arjun-manoj-2aa449251/)
- **V Harsha Vardhan**
🔗 [LinkedIn](https://www.linkedin.com/in/777hv/)

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).

---

## 🫡 Credits
- 🎵 Music from Pixabay / Mixkit (free, attribution-free)
- 🧠 Gemini API by Google
- 🗣️ TTS by Amazon Polly
- 🎛️ FFmpeg for seamless audio merging

> Built with precision, clarity, and that special military-grade polish.
