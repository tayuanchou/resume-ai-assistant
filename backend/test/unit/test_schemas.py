import pytest
from pydantic import ValidationError

from backend.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BulletSuggestion,
    JDKeywords,
    SkillMatch,
)


class TestAnalyzeRequest:
    def test_valid_request(self):
        req = AnalyzeRequest(resume_text="My resume", job_description="A job description")
        assert req.resume_text == "My resume"
        assert req.job_description == "A job description"

    def test_empty_resume_text_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(resume_text="", job_description="A job description")
        assert "resume_text must not be empty" in str(exc_info.value)

    def test_whitespace_only_resume_text_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(resume_text="   ", job_description="A job description")
        assert "resume_text must not be empty" in str(exc_info.value)

    def test_empty_job_description_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(resume_text="My resume", job_description="")
        assert "job_description must not be empty" in str(exc_info.value)

    def test_whitespace_only_job_description_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            AnalyzeRequest(resume_text="My resume", job_description="   ")
        assert "job_description must not be empty" in str(exc_info.value)


class TestJDKeywords:
    def test_construction(self):
        keywords = JDKeywords(
            required_skills=["Python"],
            preferred_skills=["AWS"],
            responsibilities=["Ship features"],
            soft_skills=["Teamwork"],
            domain_keywords=["Fintech"],
        )
        assert keywords.required_skills == ["Python"]
        assert keywords.domain_keywords == ["Fintech"]


class TestSkillMatch:
    def test_construction(self):
        match = SkillMatch(matched_skills=["Python"], missing_skills=[], weak_skills=[])
        assert match.matched_skills == ["Python"]
        assert match.missing_skills == []
        assert match.weak_skills == []


class TestBulletSuggestion:
    def test_construction(self):
        suggestion = BulletSuggestion(original="a", problem="b", improved="c")
        assert suggestion.original == "a"
        assert suggestion.problem == "b"
        assert suggestion.improved == "c"


class TestAnalyzeResponse:
    def test_construction(self):
        response = AnalyzeResponse(
            match_score=80,
            jd_keywords=JDKeywords(
                required_skills=[],
                preferred_skills=[],
                responsibilities=[],
                soft_skills=[],
                domain_keywords=[],
            ),
            skill_match=SkillMatch(matched_skills=[], missing_skills=[], weak_skills=[]),
            bullet_suggestions=[],
            tailored_summary="Summary text",
        )
        assert response.match_score == 80
        assert response.tailored_summary == "Summary text"
