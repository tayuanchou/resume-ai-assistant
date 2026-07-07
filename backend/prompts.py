JD_EXTRACTION_PROMPT = """
You are a job description analyst. Extract structured information from the following job description.

Return ONLY valid JSON with this exact structure:
{{
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill1", "skill2"],
  "responsibilities": ["responsibility1", "responsibility2"],
  "soft_skills": ["skill1", "skill2"],
  "domain_keywords": ["keyword1", "keyword2"]
}}

Job Description:
{job_description}
"""

BULLET_REWRITE_PROMPT = """
You are a professional resume coach. Review the following resume and job description.
Identify up to 3 weak bullet points in the resume and rewrite them to be more impactful.

Guidelines:
- Improve clarity, technical specificity, and impact.
- Do NOT invent fake metrics or accomplishments.
- Keep rewrites grounded in the original content.

Return ONLY valid JSON as a list:
[
  {{
    "original": "the original bullet text",
    "problem": "brief explanation of what is weak",
    "improved": "the improved version"
  }}
]

Resume:
{resume_text}

Job Description:
{job_description}
"""

SUMMARY_GENERATION_PROMPT = """
You are a professional resume writer. Write a tailored professional summary for the candidate.

Requirements:
- 2 to 4 sentences.
- Specific to the target job.
- Honest and grounded in the resume content.
- Not exaggerated or generic.

Return ONLY the summary text, no JSON, no labels.

Resume:
{resume_text}

Job Description:
{job_description}
"""
