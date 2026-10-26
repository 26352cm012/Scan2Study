# 📚 Scan2Study

Scan2Study is a study prototype that helps turn textbook material into easier-to-read text.

## Prototype experience

1. Welcome page with a guided scroll-down flow.
2. Upload a textbook image or paste text.
3. Choose **Text meaning** or **Quick study shortcut**.
4. Open a separate results page with the original material and an easier-to-read version side by side.
5. Copy either version or download both as a text file.

## How it works today

- **Frontend:** HTML, CSS, and JavaScript (\`index.html\` and \`result.html\`)
- **Full-stack option:** Python + Flask serves the page and exposes the OCR API (\`app.py\`)
- **OCR:** Tesseract.js in the browser on GitHub Pages, or Tesseract OCR through \`pytesseract\` when running with Flask
- **Easy wording:** currently a conservative set of word substitutions, not an AI-generated explanation

**Important:** The easy version will not simplify every sentence and may miss context or nuance. Check it against the textbook. AI explanations, user accounts, and saved study history are not implemented yet.

## Run the full-stack app locally

You need Python 3.10+ and the Tesseract OCR system program installed.

### 1. Install Tesseract

- **Windows:** Install Tesseract OCR and ensure its installation folder is on PATH.
- **Ubuntu/Debian:** \`sudo apt-get update && sudo apt-get install -y tesseract-ocr\`
- **macOS:** \`brew install tesseract\`

### 2. Install Python dependencies and start Flask

**Windows (Command Prompt):**

\`\`\`bat
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
\`\`\`

**macOS/Linux:**

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
\`\`\`

Then open \`http://127.0.0.1:5000\`. Flask serves both the main page and the results page.

## API endpoints

- \`GET /\` — website
- \`GET /result.html\` — comparison/results page
- \`GET /api/health\` — backend health check
- \`POST /api/process\` — process an image sent in the multipart \`image\` field

Uploaded images are limited to 10 MB and accepted as valid JPG, PNG, or WEBP. The backend processes images in memory and does not save uploaded images to disk.

## Hosting

GitHub Pages hosts the static prototype and uses browser-side OCR. It cannot run Python Flask. The Python backend can be tested locally or deployed to a Python-capable host later; no account linking is required to work on the code.

## Repository

https://github.com/26352cm012/Scan2Study
