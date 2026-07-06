from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import AnalyzeRequest, AnalyzeResponse
from backend.services.jd_analyzer import extract_jd_keywords
from backend.services.resume_matcher import match_resume_to_jd
from backend.services.bullet_rewriter import rewrite_resume_bullets, generate_tailored_summary

app = FastAPI(title="Resume AI Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    jd_keywords = extract_jd_keywords(request.job_description)

    match_result = match_resume_to_jd(request.resume_text, jd_keywords)

    bullet_suggestions = rewrite_resume_bullets(request.resume_text, request.job_description)

    tailored_summary = generate_tailored_summary(request.resume_text, request.job_description)

    return AnalyzeResponse(
        match_score=match_result["match_score"],
        jd_keywords=jd_keywords,
        skill_match={
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],
            "weak_skills": match_result["weak_skills"],
        },
        bullet_suggestions=bullet_suggestions,
        tailored_summary=tailored_summary,
    )
