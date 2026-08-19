from backend.services.resume_matcher import _count_occurrences, match_resume_to_jd


class TestCountOccurrences:
    def test_counts_whole_word_matches(self):
        assert _count_occurrences("SQL", "i know sql and sql tuning") == 2

    def test_does_not_match_substring_inside_another_word(self):
        assert _count_occurrences("SQL", "i use nosql databases") == 0

    def test_returns_zero_when_absent(self):
        assert _count_occurrences("Kubernetes", "python and react") == 0


class TestMatchResumeToJd:
    def test_required_skill_matched_when_mentioned_twice_or_more(self):
        jd_keywords = {"required_skills": ["Python"], "preferred_skills": []}
        result = match_resume_to_jd("Python developer. Wrote Python scripts.", jd_keywords)
        assert result["matched_skills"] == ["Python"]
        assert result["weak_skills"] == []
        assert result["missing_skills"] == []
        assert result["match_score"] == 100

    def test_required_skill_weak_when_mentioned_once(self):
        jd_keywords = {"required_skills": ["Python"], "preferred_skills": []}
        result = match_resume_to_jd("Python developer.", jd_keywords)
        assert result["weak_skills"] == ["Python"]
        assert result["matched_skills"] == []
        assert result["match_score"] == 0

    def test_required_skill_missing_when_not_mentioned(self):
        jd_keywords = {"required_skills": ["Kubernetes"], "preferred_skills": []}
        result = match_resume_to_jd("Python developer.", jd_keywords)
        assert result["missing_skills"] == ["Kubernetes"]
        assert result["match_score"] == 0

    def test_preferred_skill_missing_when_absent(self):
        jd_keywords = {"required_skills": [], "preferred_skills": ["AWS"]}
        result = match_resume_to_jd("Python developer.", jd_keywords)
        assert result["missing_skills"] == ["AWS"]
        assert result["weak_skills"] == []

    def test_preferred_skill_weak_when_present(self):
        jd_keywords = {"required_skills": [], "preferred_skills": ["AWS"]}
        result = match_resume_to_jd("Built systems on AWS.", jd_keywords)
        assert result["weak_skills"] == ["AWS"]
        assert result["missing_skills"] == []

    def test_match_score_zero_when_no_required_skills(self):
        jd_keywords = {"required_skills": [], "preferred_skills": []}
        result = match_resume_to_jd("Anything.", jd_keywords)
        assert result["match_score"] == 0

    def test_defaults_to_empty_lists_when_keys_missing(self):
        result = match_resume_to_jd("Anything.", {})
        assert result == {
            "matched_skills": [],
            "missing_skills": [],
            "weak_skills": [],
            "match_score": 0,
        }

    def test_match_score_rounds_to_nearest_percent(self):
        jd_keywords = {
            "required_skills": ["Python", "Java", "SQL"],
            "preferred_skills": [],
        }
        resume = "Python Python. Java Java."  # SQL missing, 2/3 required matched
        result = match_resume_to_jd(resume, jd_keywords)
        assert result["match_score"] == 67
