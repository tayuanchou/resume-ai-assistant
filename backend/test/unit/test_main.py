class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestAnalyzeEndpoint:
    def test_analyze_returns_combined_result(self, client, monkeypatch):
        monkeypatch.setattr(
            "backend.main.extract_jd_keywords",
            lambda job_description: {
                "required_skills": ["Python"],
                "preferred_skills": [],
                "responsibilities": [],
                "soft_skills": [],
                "domain_keywords": [],
            },
        )
        monkeypatch.setattr(
            "backend.main.match_resume_to_jd",
            lambda resume_text, jd_keywords: {
                "match_score": 100,
                "matched_skills": ["Python"],
                "missing_skills": [],
                "weak_skills": [],
            },
        )
        monkeypatch.setattr(
            "backend.main.rewrite_resume_bullets",
            lambda resume_text, job_description: [
                {"original": "a", "problem": "b", "improved": "c"}
            ],
        )
        monkeypatch.setattr(
            "backend.main.generate_tailored_summary",
            lambda resume_text, job_description: "Tailored summary",
        )

        response = client.post(
            "/analyze",
            json={"resume_text": "My resume", "job_description": "A job description"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["match_score"] == 100
        assert body["jd_keywords"]["required_skills"] == ["Python"]
        assert body["skill_match"]["matched_skills"] == ["Python"]
        assert body["bullet_suggestions"] == [
            {"original": "a", "problem": "b", "improved": "c"}
        ]
        assert body["tailored_summary"] == "Tailored summary"

    def test_analyze_rejects_empty_resume_text(self, client):
        response = client.post(
            "/analyze",
            json={"resume_text": "", "job_description": "A job description"},
        )
        assert response.status_code == 422

    def test_analyze_rejects_empty_job_description(self, client):
        response = client.post(
            "/analyze",
            json={"resume_text": "My resume", "job_description": ""},
        )
        assert response.status_code == 422
