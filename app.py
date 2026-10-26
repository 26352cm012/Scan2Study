import os
import time
from io import BytesIO
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from ocr import extract_text_from_image, make_study_helpers, simplify_text
from ai_explanations import AIConfigurationError, AIProviderError, generate_ai_explanation

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
CORS(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_ORIGIN", "*")}})
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Lightweight per-process throttle for this public prototype API.
_AI_CALLS_BY_IP = {}
_AI_MAX_CALLS_PER_HOUR = 15


@app.get("/")
def home():
    """Serve the frontend from the same Flask app as the API."""
    return send_from_directory(app.root_path, "index.html")

@app.get("/result.html")
def result_page():
    """Serve the dedicated side-by-side comparison page."""
    return send_from_directory(app.root_path, "result.html")

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Scan2Study API",
        "ai_enabled": bool(os.getenv("OPENAI_API_KEY", "").strip()),
    })

@app.post("/api/explain")
def explain_text():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Send study material as JSON."}), 400

    text = str(data.get("text") or "").strip()
    mode = data.get("mode", "meaning")
    if not text:
        return jsonify({"error": "Add some text to explain first."}), 400
    if len(text) > 12000:
        return jsonify({"error": "Please keep study text under 12,000 characters."}), 413
    if mode not in {"meaning", "shortcut"}:
        return jsonify({"error": "Choose a valid study mode."}), 400
    if not os.getenv("OPENAI_API_KEY", "").strip():
        return jsonify({
            "error": "The AI service is not configured yet. The site can still use its basic fallback."
        }), 503

    now = time.time()
    client_ip = (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.remote_addr
        or "unknown"
    )
    recent_calls = [
        stamp for stamp in _AI_CALLS_BY_IP.get(client_ip, [])
        if now - stamp < 3600
    ]
    if len(recent_calls) >= _AI_MAX_CALLS_PER_HOUR:
        return jsonify({
            "error": "This prototype has reached its AI request limit for this hour. Please try again later."
        }), 429
    recent_calls.append(now)
    _AI_CALLS_BY_IP[client_ip] = recent_calls

    # Periodically discard old client entries to keep the demo's memory bounded.
    if len(_AI_CALLS_BY_IP) > 1000:
        _AI_CALLS_BY_IP.clear()

    try:
        result = generate_ai_explanation(text, mode)
    except AIConfigurationError:
        return jsonify({"error": "The AI service is not configured on the backend yet."}), 503
    except AIProviderError:
        app.logger.warning("AI provider request failed.")
        return jsonify({
            "error": "The AI provider could not create an explanation right now. Please try again."
        }), 502
    except Exception:
        app.logger.exception("Unexpected AI explanation error")
        return jsonify({"error": "Something went wrong while creating the AI explanation."}), 500

    return jsonify(result)


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
        "easy_text": simplify_text(extracted_text),
        "note": "The easy version uses conservative word substitutions; it is not AI-generated and should be checked against the original."
    })

@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "Image is too large. Maximum size is 10 MB."}), 413

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
