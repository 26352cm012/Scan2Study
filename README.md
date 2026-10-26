# 📚 Scan2Study

Scan2Study turns photos of study material into searchable text and quick revision prompts.

## What works now

- Responsive frontend for uploading and previewing JPG, PNG, and WEBP images
- **Full-stack mode:** Flask serves the frontend and handles OCR through a Python API
- **Static-site mode:** GitHub Pages keeps working with browser-side Tesseract.js OCR
- Basic extractive revision notes and active-recall prompts
- Copy extracted text and download notes as a text file

**Important:** The summary and practice prompts are rule-based, not AI-generated. Accounts, cloud-saved notes, and an AI tutor are not implemented yet.

## Architecture

- **Frontend:** HTML, CSS, and JavaScript (`index.html`)
- **Backend:** Python + Flask (`app.py`)
- **OCR:** Tesseract OCR through `pytesseract`
- **Image handling:** Pillow

When the page is served by Flask, it checks `/api/health` and sends uploaded images to `/api/process`. When served as a static site such as GitHub Pages, it falls back to in-browser Tesseract.js. The Flask API processes uploads in memory and does not save the uploaded images to disk.

## Run the full-stack app locally

You need Python 3.10+ and the Tesseract OCR system program installed.

### 1. Install Tesseract

- **Windows:** Install the Tesseract OCR application and ensure its install folder is on PATH.
- **Ubuntu/Debian:** `sudo apt-get update && sudo apt-get install -y tesseract-ocr`
- **macOS:** `brew install tesseract`

### 2. Create a virtual environment and install dependencies

From the repository folder:

**Windows (Command Prompt):**

```bat
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser. The frontend and backend are served together by Flask.

### API endpoints

- `GET /` — serves the website
- `GET /api/health` — checks if the backend is running
- `POST /api/process` — processes an image sent as multipart form data in the `image` field

Example API request:

```bash
curl -X POST http://127.0.0.1:5000/api/process -F "image=@notes.jpg"
```

Images are limited to 10 MB and accepted only when they are valid JPG, PNG, or WEBP files.

## Public website vs. full-stack hosting

GitHub Pages can host the static frontend, but it cannot run Python Flask. The public GitHub Pages version therefore uses browser-side OCR. To run the frontend and Python backend together on a public URL, the Flask application must be deployed to a Python-capable web host. You do not need to link an account just to develop or run the app locally.

## Repository

https://github.com/26352cm012/Scan2Study
