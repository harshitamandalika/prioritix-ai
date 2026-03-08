import google.generativeai as genai
from backend.settings import GEMINI_API_KEY, GEMINI_TEXT_MODEL

def get_text_model():
    if not GEMINI_API_KEY:
        raise RuntimeError("Missing GEMINI_API_KEY in backend/.env")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_TEXT_MODEL)
