# Resume AI Assistant

An AI-powered backend that compares a resume against a job description, identifies skill gaps, rewrites weak bullet points, and generates a tailored professional summary.

## Tech Stack

- Python, FastAPI, Pydantic, Uvicorn
- OPEN AI API
- Plain HTML / CSS / Vanilla JavaScript frontend

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

## Running the Backend

```bash
uvicorn backend.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`.

## Debugging in VS Code

1. Open the project folder in VS Code (`File > Open Folder`).
2. Select the Python interpreter from `.venv`:
   - Press `Ctrl+Shift+P` → `Python: Select Interpreter` → choose `.venv`.
3. Go to **Run and Debug** (`Ctrl+Shift+D`).
4. Choose **Debug FastAPI Backend** from the dropdown.
5. Click the green play button (or press `F5`).
6. Open `http://127.0.0.1:8000/docs` and send a request.
7. Add breakpoints in `backend/main.py` or any file under `backend/services/` by clicking the gutter to the left of a line number.

The debugger will pause at breakpoints, letting you inspect variables and step through the request lifecycle.
