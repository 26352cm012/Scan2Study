# 📚 Scan2Study

Scan2Study turns photos of study material into searchable text and quick revision prompts.

## Current features

- Responsive browser interface for uploading and previewing notes
- Browser OCR in the website (Tesseract.js)
- Python Flask API for server-side OCR
- Basic extractive revision notes and active-recall prompts
- Copy extracted text and download notes as a text file

**Important:** Summaries and practice prompts are rule-based, not AI-generated. Accounts, cloud-saved notes, and an AI tutor are not implemented yet.

## Architecture

- **Frontend:** HTML, CSS, JavaScript, hosted on GitHub Pages
- **Backend:** Python + Flask (app.py)
- **OCR:** Tesseract OCR through pytesseract
- **Image handling:** Pillow

## Run the backend locally

You need Python 3.10+ and the Tesseract OCR system program installed.

### 1. Install Tesseract

- **Windows:** Install the Tesseract OCR application and ensure its install folder is on PATH.
- **Ubuntu/Debian:** sudo apt-get update && sudo apt-get install -y tesseract-ocr
- **macOS:** brew install tesseract

### 2. Install Python packages and start the API

    python -m venv .venv
    # Windows: .venv\\Scripts\\activate
    # macOS/Linux: source .venv/bin/activate
    pip install -r requirements.txt
    python app.py

The API will be available at http://127.0.0.1:5000.

- Health check: GET /api/health
- Process an image: POST /api/process using multipart form data with an image file field

Example with curl:

    curl -X POST http://127.0.0.1:5000/api/process -F "image=@notes.jpg"

## Deploy the backend on Render

This repository includes a render.yaml blueprint and apt.txt for the Tesseract system dependency.

1. Sign in to Render and create a new Blueprint from this GitHub repository.
2. Review the service settings from render.yaml and deploy.
3. Test https://YOUR-SERVICE.onrender.com/api/health after deployment.
4. The configured FRONTEND_ORIGIN is https://26352cm012.github.io.

GitHub Pages hosts only the static frontend. Adding this API does not automatically make the current page call the backend; the current page continues using browser-side Tesseract.js until it is configured with the deployed API URL.

## Repository

https://github.com/26352cm012/Scan2Study
