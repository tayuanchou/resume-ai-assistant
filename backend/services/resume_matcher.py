import re


def _count_occurrences(skill: str, resume_lower: str) -> int:
    # Negative lookbehind/lookahead prevents partial-word matches (e.g. "SQL" inside "NoSQL")
    pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
    return len(re.findall(pattern, resume_lower))


def match_resume_to_jd(resume_text: str, jd_keywords: dict) -> dict:
    resume_lower = resume_text.lower()

    required_skills = jd_keywords.get("required_skills", [])
    preferred_skills = jd_keywords.get("preferred_skills", [])

    matched: list[str] = []
    weak: list[str] = []
    missing: list[str] = []

    for skill in required_skills:
        count = _count_occurrences(skill, resume_lower)
        if count >= 2:
            matched.append(skill)
        elif count == 1:
            weak.append(skill)
        else:
            missing.append(skill)

    # Preferred skills don't affect the score but surface as weak/missing
    for skill in preferred_skills:
        count = _count_occurrences(skill, resume_lower)
        if count == 0:
            missing.append(skill)
        else:
            weak.append(skill)

    total_required = len(required_skills)
    match_score = round(len(matched) / total_required * 100) if total_required > 0 else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "weak_skills": weak,
        "match_score": match_score,
    }
