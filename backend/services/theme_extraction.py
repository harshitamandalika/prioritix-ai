import json
from backend.services.gemini_client import get_text_model

def safe_json_load(s: str):
    s = s.strip()
    # handle accidental code fences
    if s.startswith("```"):
        s = s.split("```")[1]
    return json.loads(s)

def extract_theme(text: str) -> dict:
    prompt = open("backend/prompts/theme_extraction.txt", "r", encoding="utf-8").read()
    prompt = prompt.replace("{{text}}", text)

    model = get_text_model()
    resp = model.generate_content(prompt)
    return safe_json_load(resp.text)
