"""OCR and basic study-helper functions for Scan2Study."""
import re
import pytesseract
from PIL import Image

def extract_text_from_image(image: Image.Image) -> str:
    """Extract English text from a PIL image using the system Tesseract OCR engine."""
    return pytesseract.image_to_string(image, lang="eng")

def make_study_helpers(text: str, limit: int = 5):
    """Create simple extractive revision notes and recall prompts, not AI output."""
    sentences = [
        item.strip()
        for item in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text))
        if len(item.strip()) > 25
    ]
    summary = sentences[:limit] or ([text[:500]] if text else [])
    questions = [
        "Can you explain this in your own words: " + sentence
        for sentence in sentences[:limit]
    ] or (["What are the main ideas in these notes?"] if text else [])
    return summary, questions
