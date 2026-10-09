import os
from io import BytesIO
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from ocr import extract_text_from_image, make_study_helpers

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
CORS(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_ORIGIN", "*")}})
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

@app.get("/")
def home():
    return jsonify({"name": "Scan2Study API", "status": "running",
                    "endpoints": ["/api/health", "/api/process"]})

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Scan2Study API"})

@app.post("/api/process")
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "Upload an image using the 'image' field."}), 400
    uploaded = request.files["image"]
    if not uploaded.filename:
        return jsonify({"error": "Choose an image file first."}), 400
    if uploaded.mimetype not in ALLOWED_MIME_TYPES:
        return jsonify({"error": "Only JPG, PNG, and WEBP images are supported."}), 415
    try:
        raw = uploaded.read()
        if not raw:
            return jsonify({"error": "The uploaded file is empty."}), 400
        image = Image.open(BytesIO(raw))
        image.verify()
        image = Image.open(BytesIO(raw)).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify({"error": "That file is not a valid image."}), 400
    try:
        extracted_text = extract_text_from_image(image).strip()
    except Exception:
        app.logger.exception("OCR processing failed")
        return jsonify({"error": "OCR failed. Please try a clearer photo."}), 500
    if not extracted_text:
        return jsonify({"error": "No text found. Try a brighter, sharper photo."}), 422
    summary, questions = make_study_helpers(extracted_text)
    return jsonify({
        "extracted_text": extracted_text,
        "summary": summary,
        "questions": questions,
        "note": "Summary and practice prompts are rule-based, not AI-generated."
    })

@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "Image is too large. Maximum size is 10 MB."}), 413

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
