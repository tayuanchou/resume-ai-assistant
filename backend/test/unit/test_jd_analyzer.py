import json

import pytest

from backend.services import jd_analyzer


class _FakeMessage:
    def __init__(self, content):
        self.content = content


class _FakeChoice:
    def __init__(self, content):
        self.message = _FakeMessage(content)


class _FakeCompletionResponse:
    def __init__(self, content):
        self.choices = [_FakeChoice(content)]


class _FakeCompletions:
    def __init__(self, content=None, raise_exc=None):
        self._content = content
        self._raise_exc = raise_exc

    def create(self, **kwargs):
        if self._raise_exc:
            raise self._raise_exc
        return _FakeCompletionResponse(self._content)


class _FakeChat:
    def __init__(self, completions):
        self.completions = completions


class _FakeOpenAIClient:
    def __init__(self, content=None, raise_exc=None, **kwargs):
        self.chat = _FakeChat(_FakeCompletions(content=content, raise_exc=raise_exc))


def _make_fake_openai(content=None, raise_exc=None):
    def _factory(*args, **kwargs):
        return _FakeOpenAIClient(content=content, raise_exc=raise_exc)

    return _factory


class TestEmptyKeywords:
    def test_returns_all_empty_lists(self):
        assert jd_analyzer._empty_keywords() == {
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "soft_skills": [],
            "domain_keywords": [],
        }


class TestFallbackKeywordExtraction:
    def test_finds_known_skills_case_insensitively(self):
        jd = "We need someone with Python, sql and REACT experience."
        result = jd_analyzer._fallback_keyword_extraction(jd)
        assert result["required_skills"] == ["Python", "SQL", "React"]
        assert result["preferred_skills"] == []
        assert result["responsibilities"] == []
        assert result["soft_skills"] == []
        assert result["domain_keywords"] == []

    def test_no_known_skills_found(self):
        result = jd_analyzer._fallback_keyword_extraction("We need a great communicator.")
        assert result["required_skills"] == []

    def test_single_entry_when_skill_mentioned_multiple_times(self):
        result = jd_analyzer._fallback_keyword_extraction("Python Python python PYTHON")
        assert result["required_skills"] == ["Python"]


class TestParseAiJsonResponse:
    @staticmethod
    def _valid_payload():
        return {
            "required_skills": ["Python", "Python"],
            "preferred_skills": ["AWS"],
            "responsibilities": ["Build things"],
            "soft_skills": ["Communication"],
            "domain_keywords": ["Fintech"],
        }

    def test_parses_plain_json_and_dedupes_lists(self):
        result = jd_analyzer._parse_ai_json_response(json.dumps(self._valid_payload()))
        assert result["required_skills"] == ["Python"]
        assert result["preferred_skills"] == ["AWS"]

    def test_strips_markdown_code_fences_with_json_tag(self):
        wrapped = f"```json\n{json.dumps(self._valid_payload())}\n```"
        result = jd_analyzer._parse_ai_json_response(wrapped)
        assert result["domain_keywords"] == ["Fintech"]

    def test_strips_code_fences_without_language_tag(self):
        wrapped = f"```\n{json.dumps(self._valid_payload())}\n```"
        result = jd_analyzer._parse_ai_json_response(wrapped)
        assert result["responsibilities"] == ["Build things"]

    def test_raises_when_missing_required_keys(self):
        with pytest.raises(ValueError):
            jd_analyzer._parse_ai_json_response(json.dumps({"required_skills": []}))

    def test_raises_when_not_a_dict(self):
        with pytest.raises(ValueError):
            jd_analyzer._parse_ai_json_response(json.dumps(["not", "a", "dict"]))

    def test_raises_on_malformed_json(self):
        with pytest.raises(json.JSONDecodeError):
            jd_analyzer._parse_ai_json_response("not valid json")


class TestExtractJdKeywords:
    def test_falls_back_when_no_api_key(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = jd_analyzer.extract_jd_keywords("Looking for a Python developer.")
        assert result["required_skills"] == ["Python"]

    def test_uses_openai_response_when_api_key_present(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        payload = {
            "required_skills": ["Python"],
            "preferred_skills": ["AWS"],
            "responsibilities": ["Ship features"],
            "soft_skills": ["Teamwork"],
            "domain_keywords": ["Fintech"],
        }
        monkeypatch.setattr(
            jd_analyzer, "OpenAI", _make_fake_openai(content=json.dumps(payload))
        )
        result = jd_analyzer.extract_jd_keywords("A job description.")
        assert result == payload

    def test_falls_back_when_openai_raises(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setattr(
            jd_analyzer, "OpenAI", _make_fake_openai(raise_exc=RuntimeError("boom"))
        )
        result = jd_analyzer.extract_jd_keywords("Looking for a Python developer.")
        assert result["required_skills"] == ["Python"]

    def test_falls_back_when_response_content_is_none(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setattr(jd_analyzer, "OpenAI", _make_fake_openai(content=None))
        result = jd_analyzer.extract_jd_keywords("Looking for a Python developer.")
        assert result["required_skills"] == ["Python"]

    def test_falls_back_when_response_is_malformed_json(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setattr(jd_analyzer, "OpenAI", _make_fake_openai(content="not json"))
        result = jd_analyzer.extract_jd_keywords("Looking for a Python developer.")
        assert result["required_skills"] == ["Python"]
