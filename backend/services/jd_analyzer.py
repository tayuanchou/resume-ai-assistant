import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from backend.prompts import JD_EXTRACTION_PROMPT


load_dotenv()

_KNOWN_TECH_SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "SQL", "PostgreSQL", "MySQL",
    "FastAPI", "Flask", "Django", "React", "Node.js", "Express", "AWS", "Docker",
    "Kubernetes", "Git", "CI/CD", "REST APIs", "GraphQL", "Firebase", "GCP", "Azure",
]


def _empty_keywords() -> dict:
    return {
        "required_skills": [],
        "preferred_skills": [],
        "responsibilities": [],
        "soft_skills": [],
        "domain_keywords": [],
    }


def _fallback_keyword_extraction(job_description: str) -> dict:
    text_lower = job_description.lower()
    found = [skill for skill in _KNOWN_TECH_SKILLS if skill.lower()
             in text_lower]
    result = _empty_keywords()
    result["required_skills"] = list(
        dict.fromkeys(found))  # preserves order, dedupes
    return result


def _parse_ai_json_response(response_text: str) -> dict:
    # Strip markdown code fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "",
                     response_text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())

    data = json.loads(cleaned)

    expected_keys = {"required_skills", "preferred_skills",
                     "responsibilities", "soft_skills", "domain_keywords"}
    if not isinstance(data, dict) or not expected_keys.issubset(data.keys()):
        raise ValueError("AI response missing required keys")

    # Deduplicate each list
    for key in expected_keys:
        data[key] = list(dict.fromkeys(data.get(key, [])))

    return data


def extract_jd_keywords(job_description: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_keyword_extraction(job_description)

    try:
        client = OpenAI(api_key=api_key)
        prompt = JD_EXTRACTION_PROMPT.format(job_description=job_description)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        response_text = response.choices[0].message.content or ""
        return _parse_ai_json_response(response_text)

    except Exception:
        return _fallback_keyword_extraction(job_description)
