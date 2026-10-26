# 📚 Scan2Study

Scan2Study is a study prototype that helps turn textbook material into easier-to-read text.

## Prototype experience

1. Welcome page with a guided scroll-down flow.
2. Upload a textbook image or paste text.
3. Choose **Text meaning** or **Quick study shortcut**.
4. Open a separate results page with the original material and an easier-to-read version side by side.
5. Copy either version or download both as a text file.
6. Use the **Ask Scan2Study** chat section to ask questions and follow up, when the AI backend is configured.

## How it works today

- **Frontend:** HTML, CSS, and JavaScript (\`index.html\` and \`result.html\`)
- **Full-stack option:** Python + Flask serves the page and exposes the OCR API (\`app.py\`)
- **OCR:** Tesseract.js in the browser on GitHub Pages, or Tesseract OCR through \`pytesseract\` when running with Flask
- **AI explanations:** the Flask backend can call the OpenAI Responses API when `OPENAI_API_KEY` is configured server-side. The selected study mode controls whether it returns a plain-language explanation or an explanation plus a study shortcut.
- **Fallback:** if the backend or AI service is not connected, the static GitHub Pages site uses conservative word substitutions, not an AI-generated explanation.

**Important:** Genuine AI explanations only work when a running Flask backend has a valid `OPENAI_API_KEY` and the frontend is configured to reach that backend. Without both, the website uses basic word substitutions. AI output can be wrong, so check it against the textbook. User accounts and saved study history are not implemented.

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

## Enable genuine AI explanations

1. Deploy the Flask app to a Python-capable host (the included `render.yaml` describes the service).
2. In the backend host's environment settings, add `OPENAI_API_KEY` with your own secret API key. Optionally set `OPENAI_MODEL` to a model available to your API account. Never commit the key to GitHub or place it in `index.html` or `config.js`.
3. Set `apiBaseUrl` in `config.js` to the public base URL of the deployed Flask backend, then deploy the static site again. This URL is public; it must not contain a key.
4. Open the site and try pasted text first. The backend health endpoint reports whether the AI key is configured.

GitHub Pages hosts the static frontend and browser-side OCR; it cannot run Python Flask itself. If the backend is not deployed/configured, the site deliberately falls back to basic word substitutions. You do not need to link a GitHub account to a hosting provider to edit or prepare the code, but the backend must run somewhere for live AI calls. A public demo API can incur usage costs, so protect the key, monitor usage, and keep request limits enabled.

## Repository

https://github.com/26352cm012/Scan2Study
