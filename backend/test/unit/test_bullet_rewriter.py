from backend.services.bullet_rewriter import (
    generate_tailored_summary,
    rewrite_resume_bullets,
)


class TestRewriteResumeBullets:
    def test_returns_empty_list(self):
        assert rewrite_resume_bullets("resume text", "job description") == []


class TestGenerateTailoredSummary:
    def test_returns_empty_string(self):
        assert generate_tailored_summary("resume text", "job description") == ""
