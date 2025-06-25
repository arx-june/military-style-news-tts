# utils/genai_utils.py

import os
import logging
import google.generativeai as genai

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

# Choose your model
MODEL_NAME = "gemini-2.5-flash"  # or "gemini-live-2.5-flash"

def extract_and_summarize(image_path: str) -> str:
    """
    Extracts text from an image and returns a concise summary
    with a galvanizing military-style dispatch.

    Args:
        image_path: Path to a JPEG image file containing text.
    Returns:
        A single, coherent paragraph combining the summary
        and a high-octane military dialogue.
    Raises:
        Exception: If file handling or API call fails.
    """
    print(f"DEBUG: Processing image: {image_path}")

    if not os.path.exists(image_path):
        raise Exception(f"Image file not found: {image_path}")

    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()

        prompt = (
            "You are a cutting-edge text extraction and summarization engine armed with a "
            "battle-hardened, strategic mindset. I will supply you with an image containing a "
            "critical news article. Your mission is to first extract every detail of the text "
            "from the image with flawless precision, preserving line breaks, punctuation, and "
            "spacing exactly as they appear. Then, distill the core intelligence into a concise, "
            "razor-sharp summary that captures the essence of the news. Following that, craft a "
            "powerful, galvanizing military dispatch that amplifies the summary and ignites "
            "unyielding determination, valor, and strategic resolve—much like rallying an elite "
            "strike force on the frontline. The final output must be a single, coherent paragraph "
            "that seamlessly fuses the succinct news summary with the resolute, high-octane "
            "military dialogue. Do not include the full extracted text, and avoid any extraneous "
            "formatting characters such as numbers or asterisks; only use plain characters, "
            "punctuation, and spaces."
        )

        # Initialize the model for each call (just like your original code)
        model = genai.GenerativeModel(MODEL_NAME)

        contents = [{
            "parts": [
                prompt,
                {"mime_type": "image/jpeg", "data": img_bytes}
            ]
        }]

        response = model.generate_content(contents)
        return response.text

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise Exception(f"Text extraction failed: {str(e)}")
