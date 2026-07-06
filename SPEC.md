# Resume AI Assistant — Project Specification

## 1. Project Overview

**Resume AI Assistant** is a small AI-powered backend project that compares a user's resume against a target job description. The application extracts key skills from the job description, matches them against the resume, identifies missing or weakly represented skills, rewrites weak resume bullet points, and generates a tailored professional summary.

The project is designed as a backend-focused portfolio project using **FastAPI**, a simple **HTML/JavaScript frontend**, and an AI API such as **OpenAI API** or **Claude API**.

The main goal is to demonstrate backend API design, structured JSON responses, AI prompt orchestration, text-processing logic, and an end-to-end product workflow.

---

## 2. Target User

The target user is a job seeker who wants to tailor their resume to a specific job description.

The user should be able to:

1. Paste their resume text.
2. Paste a job description.
3. Click an Analyze button.
4. Receive structured feedback showing:
   - Job description keywords.
   - Resume-to-JD match score.
   - Matched skills.
   - Missing skills.
   - Weakly represented skills.
   - Improved resume bullet points.
   - A tailored professional summary.

---

## 3. Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Python-dotenv
- OpenAI API or Claude API

### Frontend

- Plain HTML
- CSS
- Vanilla JavaScript
- Fetch API

### Data Format

- JSON request body
- JSON response body

### API Documentation

- FastAPI Swagger UI
- Available at `/docs`

---

## 4. Project Structure

```text
resume-ai-assistant/
│
├── backend/
│   ├── main.py
│   ├── schemas.py
│   ├── prompts.py
│   │
│   └── services/
│       ├── jd_analyzer.py
│       ├── resume_matcher.py
│       └── bullet_rewriter.py
│
├── frontend/
│   └── index.html
│
├── README.md
├── SPEC.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 5. Core Features

### Feature 1: Resume and Job Description Input

The frontend should provide two large text areas:

1. Resume text input.
2. Job description text input.

The user should click an **Analyze** button to send both text inputs to the backend.

The backend should expose one main endpoint:

```http
POST /analyze
```

Request body:

```json
{
  "resume_text": "string",
  "job_description": "string"
}
```

Validation rules:

- `resume_text` is required.
- `job_description` is required.
- Both fields must be non-empty strings.
- If either field is empty, return a clear validation error.

---

### Feature 2: Job Description Keyword Extraction

The backend should extract important information from the job description.

The extracted information should include:

- Required technical skills.
- Preferred technical skills.
- Responsibilities.
- Soft skills.
- Domain keywords.

Example output:

```json
{
  "required_skills": ["Python", "FastAPI", "SQL", "REST APIs"],
  "preferred_skills": ["AWS", "Docker", "CI/CD"],
  "responsibilities": [
    "Build backend services",
    "Develop APIs",
    "Collaborate with cross-functional teams"
  ],
  "soft_skills": ["communication", "collaboration"],
  "domain_keywords": ["backend development", "cloud services"]
}
```

Implementation notes:

- Use an AI API to extract structured JSON from the job description.
- The AI output must be parsed into a predictable Python dictionary.
- If the AI response fails or returns invalid JSON, the backend should return a graceful fallback response rather than crashing.

Relevant file:

```text
backend/services/jd_analyzer.py
```

Main function:

```python
def extract_jd_keywords(job_description: str) -> dict:
    ...
```

---

### Feature 3: Resume Skill Matching

The backend should compare extracted job description skills against the resume text.

The matching logic should return:

- Matched skills.
- Missing skills.
- Weakly represented skills.
- Match score.

The initial matching logic can be simple keyword matching.

Example output:

```json
{
  "matched_skills": ["Python", "SQL", "REST APIs"],
  "missing_skills": ["Docker", "AWS"],
  "weak_skills": ["CI/CD"],
  "match_score": 60
}
```

Suggested match score formula:

```text
match_score = matched_required_skills / total_required_skills * 100
```

If there are no required skills, return a score of `0`.

Implementation notes:

- Normalize text to lowercase before matching.
- Match required skills first.
- Preferred skills may be included in missing skills or weak skills but should not dominate the score.
- Keep this logic deterministic rather than fully AI-based, so the project demonstrates backend logic.

Relevant file:

```text
backend/services/resume_matcher.py
```

Main function:

```python
def match_resume_to_jd(resume_text: str, jd_keywords: dict) -> dict:
    ...
```

---

### Feature 4: Resume Bullet Rewrite Suggestions

The backend should use AI to identify weak resume bullets and rewrite them.

The AI should return up to 3 rewritten bullet suggestions.

Each suggestion should include:

- Original bullet.
- Problem with the bullet.
- Improved bullet.

Example output:

```json
[
  {
    "original": "Worked on backend APIs and fixed bugs.",
    "problem": "Too vague and lacks technical detail or impact.",
    "improved": "Developed and maintained RESTful backend APIs to support business-critical workflows, improving reliability across production data operations."
  }
]
```

Implementation notes:

- The AI should focus on improving clarity, technical specificity, and impact.
- The rewritten bullets should not invent fake metrics.
- If no clear bullet points are found, the system should still return general improvement suggestions.

Relevant file:

```text
backend/services/bullet_rewriter.py
```

Main function:

```python
def rewrite_resume_bullets(resume_text: str, job_description: str) -> list[dict]:
    ...
```

---

### Feature 5: Tailored Resume Summary

The backend should generate a short tailored professional summary based on the resume and job description.

The summary should be:

- 2 to 4 sentences.
- Specific to the target job.
- Honest and grounded in the resume.
- Not overly exaggerated.

Example output:

```json
{
  "tailored_summary": "Software Engineer with experience building backend APIs, implementing business logic, managing database migrations, and supporting production data workflows. Skilled in Python, SQL, REST API development, and cross-environment validation, with growing experience in AI-assisted engineering tools."
}
```

This can be implemented in the same service as bullet rewriting or in a separate helper function.

Suggested function:

```python
def generate_tailored_summary(resume_text: str, job_description: str) -> str:
    ...
```

---

## 6. Main API Contract

### Endpoint

```http
POST /analyze
```

### Request

```json
{
  "resume_text": "string",
  "job_description": "string"
}
```

### Successful Response

```json
{
  "match_score": 76,
  "jd_keywords": {
    "required_skills": ["Python", "FastAPI", "SQL", "REST APIs"],
    "preferred_skills": ["AWS", "Docker"],
    "responsibilities": [
      "Build backend services",
      "Develop APIs",
      "Collaborate with engineers"
    ],
    "soft_skills": ["communication", "collaboration"],
    "domain_keywords": ["backend development", "cloud services"]
  },
  "skill_match": {
    "matched_skills": ["Python", "SQL", "REST APIs"],
    "missing_skills": ["FastAPI", "AWS", "Docker"],
    "weak_skills": ["CI/CD"]
  },
  "bullet_suggestions": [
    {
      "original": "Worked on backend APIs.",
      "problem": "Too vague and lacks technical detail.",
      "improved": "Developed RESTful backend APIs to support business-critical workflows and improve maintainability across backend services."
    }
  ],
  "tailored_summary": "Software Engineer with backend development experience in API implementation, SQL-based workflows, and production issue resolution."
}
```

### Error Response

```json
{
  "detail": "Resume text and job description are required."
}
```

---

## 7. Backend File Responsibilities

### `backend/main.py`

Responsibilities:

- Create FastAPI app.
- Configure CORS if needed.
- Define `/health` endpoint.
- Define `/analyze` endpoint.
- Call service-layer functions.
- Return structured response.

Required endpoints:

```http
GET /health
POST /analyze
```

---

### `backend/schemas.py`

Responsibilities:

- Define Pydantic request and response models.

Suggested models:

```python
class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str
```

Optional models:

```python
class JDKeywords(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    soft_skills: list[str]
    domain_keywords: list[str]
```

---

### `backend/prompts.py`

Responsibilities:

- Store reusable AI prompts.
- Keep prompt text separate from business logic.

Suggested constants:

```python
JD_EXTRACTION_PROMPT = ...
BULLET_REWRITE_PROMPT = ...
SUMMARY_GENERATION_PROMPT = ...
```

---

### `backend/services/jd_analyzer.py`

Responsibilities:

- Call AI API to extract JD keywords.
- Parse AI response into dictionary.
- Return fallback response if AI parsing fails.

---

### `backend/services/resume_matcher.py`

Responsibilities:

- Compare resume text with extracted JD skills.
- Calculate match score.
- Return matched, missing, and weak skills.

---

### `backend/services/bullet_rewriter.py`

Responsibilities:

- Call AI API to rewrite weak resume bullets.
- Generate tailored resume summary.
- Return structured suggestions.

---

### `frontend/index.html`

Responsibilities:

- Render resume textarea.
- Render job description textarea.
- Send POST request to backend `/analyze`.
- Display analysis result in readable sections.

Required frontend sections:

- Match score.
- JD keywords.
- Matched skills.
- Missing skills.
- Weak skills.
- Bullet suggestions.
- Tailored summary.

---

## 8. Environment Variables

The project should use a `.env` file for API keys.

`.env.example`:

```text
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=openai
```

Optional:

```text
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

The real `.env` file must not be committed to GitHub.

---

## 9. Requirements File

`requirements.txt` should include:

```text
fastapi
uvicorn
pydantic
python-dotenv
openai
```

Optional if using Claude API:

```text
anthropic
```

---

## 10. Local Development Commands

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Windows Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn backend.main:app --reload
```

Open Swagger docs:

```text
http://127.0.0.1:8000/docs
```

Open frontend:

```text
frontend/index.html
```

If browser CORS or local file issues occur, serve the frontend with:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500/frontend/index.html
```

---

## 11. MVP Acceptance Criteria

The project is considered complete when:

1. GitHub repo exists.
2. FastAPI backend runs locally.
3. `/health` returns a success response.
4. `/analyze` accepts resume text and job description text.
5. The backend returns structured JSON.
6. JD keyword extraction works.
7. Resume skill matching works.
8. Match score is calculated.
9. Bullet rewrite suggestions are returned.
10. Tailored summary is returned.
11. Simple HTML frontend can call the backend.
12. README explains the project, setup, features, API, and future improvements.

---

## 12. Non-Goals for MVP

Do not implement these in the first 6-hour version:

- User login.
- Database persistence.
- PDF upload.
- DOCX upload.
- Resume template rendering.
- Export to PDF.
- Payment.
- User dashboard.
- React frontend.
- Deployment.

These are future improvements, not MVP requirements.

---

## 13. Suggested Implementation Order

### Phase 1: Repository and Project Setup

1. Create GitHub repo.
2. Initialize local project.
3. Create folder structure.
4. Add `.gitignore`, `.env.example`, `requirements.txt`, and `README.md`.

### Phase 2: FastAPI Skeleton

1. Create FastAPI app.
2. Add `/health`.
3. Add `/analyze` with mock response.
4. Confirm Swagger UI works.

### Phase 3: JD Analyzer

1. Add prompt for JD keyword extraction.
2. Call AI API.
3. Parse structured JSON.
4. Return fallback JSON on failure.

### Phase 4: Resume Matcher

1. Normalize resume text.
2. Compare required skills against resume.
3. Compare preferred skills against resume.
4. Return matched, missing, weak skills.
5. Calculate match score.

### Phase 5: Bullet Rewriter and Summary Generator

1. Add AI prompt for bullet rewriting.
2. Return up to 3 bullet suggestions.
3. Add tailored summary generation.

### Phase 6: Frontend

1. Build simple HTML page.
2. Add resume textarea.
3. Add job description textarea.
4. Add Analyze button.
5. Call backend using fetch.
6. Render returned JSON in readable sections.

### Phase 7: README Polish

1. Add project overview.
2. Add feature list.
3. Add tech stack.
4. Add setup instructions.
5. Add API contract.
6. Add future improvements.

---

## 14. Claude Code Instruction

Use this project specification to build the MVP version of Resume AI Assistant.

Prioritize working software over perfect architecture.

Implement the project in this order:

1. Create the folder structure.
2. Implement FastAPI backend skeleton.
3. Add request and response schemas.
4. Implement `/health`.
5. Implement `/analyze` with mock response first.
6. Implement deterministic resume skill matching.
7. Implement AI-based JD keyword extraction.
8. Implement AI-based bullet rewriting.
9. Implement tailored summary generation.
10. Build simple HTML frontend.
11. Update README.

Keep the code simple, readable, and modular.

Do not add login, database, PDF upload, React, or deployment in the MVP.
