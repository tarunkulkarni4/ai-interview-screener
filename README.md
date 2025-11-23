# Mini AI Interview Screener (Backend Only)

A lightweight backend service that evaluates candidate answers using an LLM (OpenAI optional) or a fallback rule-based evaluator. This README contains only the core setup and usage steps — no email, no video, no API key instructions.

---

## 1. Project Structure

```
main.py          # FastAPI endpoints and models
scorer.py        # Cleans input + calls evaluator
llm_client.py    # LLM + fallback evaluation
requirements.txt # Dependencies
.env.example     # Example environment file
README.md        # This file
```

---

## 2. Setup Instructions (Windows)

### Step 1 — Go to your project folder

```powershell
cd C:\Users\91963\ai-screener\ai-screener
```

### Step 2 — Create & activate virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Optional `.env`

```powershell
notepad .env
```

(Do not commit this file.)

---

## 3. Run the Server

```powershell
uvicorn main:app --reload --port 8000
```

Open Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 4. API Examples

### POST `/evaluate-answer`

```json
{
  "answer": "Candidate says: REST APIs use GET and POST methods.",
  "question": "Explain REST APIs."
}
```

### POST `/rank-candidates`

```json
[
  {"id": "c1", "answer": "Candidate says: Use REST and Express."},
  {"id": "c2", "answer": "Candidate says: Use REST, proper status codes, and examples."}
]
```

---

## 5. GitHub Push Instructions (Safe)

### Step 1 — Initialize repo

```powershell
git init
git add .
git commit -m "initial commit"
```

### Step 2 — Create repo on GitHub

Go to: [https://github.com/new](https://github.com/new)

### Step 3 — Add remote

```powershell
git remote add origin https://github.com/<your-username>/ai-interview-screener.git
```

### Step 4 — Ensure `.env` is not tracked

```powershell
git rm --cached .env
```

Add to `.gitignore`:

```
.env
venv/
__pycache__/
```

### Step 5 — Push

```powershell
git add .
git commit -m "ready"
git push -u origin main
```

---

## 6. Done

The backend is ready for testing and review. Let me know if you want enhancements like Docker, deployment, or Swagger improvements.
