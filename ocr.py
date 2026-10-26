"""OCR and conservative, rule-based text helpers for Scan2Study."""
import re
import pytesseract
from PIL import Image

# Conservative swaps for selected formal terms. This is not an AI model.
_REPLACEMENTS = [
    ("due to the fact that", "because"),
    ("as a consequence of", "because of"),
    ("at this point in time", "now"),
    ("for the purpose of", "to"),
    ("in the event that", "if"),
    ("subsequent to", "after"),
    ("prior to", "before"),
    ("in addition to", "also"),
    ("make use of", "use"),
    ("is characterized by", "has"),
    ("is defined as", "means"),
    ("consists of", "is made of"),
    ("can be observed", "we can see"),
    ("has the ability to", "can"),
    ("it is necessary to", "we need to"),
    ("approximately", "about"),
    ("demonstrate", "show"),
    ("demonstrates", "shows"),
    ("illustrates", "shows"),
    ("facilitate", "help"),
    ("utilization", "use"),
    ("utilize", "use"),
    ("commence", "start"),
    ("terminate", "end"),
    ("sufficient", "enough"),
    ("obtain", "get"),
    ("assist", "help"),
    ("indicate", "show"),
    ("occur", "happen"),
    ("essential", "important"),
    ("numerous", "many"),
    ("individuals", "people"),
    ("predominantly", "mostly"),
    ("substantial", "large"),
    ("fundamental", "basic"),
    ("methodology", "method"),
    ("synthesize", "combine"),
    ("therefore", "so"),
    ("however", "but"),
    ("consequently", "as a result"),
    ("require", "need"),
]

def extract_text_from_image(image: Image.Image) -> str:
    """Extract English text from a PIL image using the system Tesseract OCR engine."""
    return pytesseract.image_to_string(image, lang="eng")

def simplify_text(text: str) -> str:
    """Apply a small set of conservative plain-language substitutions."""
    result = text
    for original, replacement in sorted(_REPLACEMENTS, key=lambda pair: len(pair[0]), reverse=True):
        pattern = re.compile(r"(?<!\w)" + re.escape(original) + r"(?!\w)", re.IGNORECASE)
        def replace(match, value=replacement):
            replacement_text = value
            if match.group(0)[:1].isupper():
                replacement_text = replacement_text[:1].upper() + replacement_text[1:]
            return replacement_text
        result = pattern.sub(replace, result)
    return result

def make_study_helpers(text: str, limit: int = 5):
    """Create simple extractive revision notes and recall prompts, not AI output."""
    sentences = [
        item.strip()
        for item in re.split(r"(?<=[.!?])\s+", re.sub(r"[ \t]+", " ", text))
        if len(item.strip()) > 25
    ]
    summary = sentences[:limit] or ([text[:500]] if text else [])
    questions = [
        "Can you explain this in your own words: " + sentence
        for sentence in sentences[:limit]
    ] or (["What are the main ideas in these notes?"] if text else [])
    return summary, questions
