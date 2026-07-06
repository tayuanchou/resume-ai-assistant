from pydantic import BaseModel, field_validator


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str

    @field_validator("resume_text", "job_description")
    @classmethod
    def must_not_be_empty(cls, v: str, info) -> str:
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v


class JDKeywords(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    soft_skills: list[str]
    domain_keywords: list[str]


class SkillMatch(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    weak_skills: list[str]


class BulletSuggestion(BaseModel):
    original: str
    problem: str
    improved: str


class AnalyzeResponse(BaseModel):
    match_score: int
    jd_keywords: JDKeywords
    skill_match: SkillMatch
    bullet_suggestions: list[BulletSuggestion]
    tailored_summary: str
