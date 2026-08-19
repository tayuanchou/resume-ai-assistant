from backend import prompts


class TestJdExtractionPrompt:
    def test_formats_with_job_description(self):
        rendered = prompts.JD_EXTRACTION_PROMPT.format(job_description="Some JD text")
        assert "Some JD text" in rendered
        assert "required_skills" in rendered


class TestBulletRewritePrompt:
    def test_formats_with_resume_and_job_description(self):
        rendered = prompts.BULLET_REWRITE_PROMPT.format(
            resume_text="My resume", job_description="Some JD text"
        )
        assert "My resume" in rendered
        assert "Some JD text" in rendered


class TestSummaryGenerationPrompt:
    def test_formats_with_resume_and_job_description(self):
        rendered = prompts.SUMMARY_GENERATION_PROMPT.format(
            resume_text="My resume", job_description="Some JD text"
        )
        assert "My resume" in rendered
        assert "Some JD text" in rendered
