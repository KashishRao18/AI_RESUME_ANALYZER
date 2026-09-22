"""
AI Resume Analyzer — Flask backend
-----------------------------------
Endpoints
  POST /api/analyze
      multipart/form-data:
        resume          -> file (.pdf, .docx, .txt)
        job_description  -> text
      returns JSON with extracted skills, match score, gaps, and a summary.

  GET  /api/health
      simple liveness check.

Resume parsing:  pdfplumber (PDF) / python-docx (DOCX) / plain text
Skill extraction: rule-based matcher over skill_data.FLAT_SKILLS (fast, free,
                   works offline)
GenAI layer:      if ANTHROPIC_API_KEY is set in the environment, the backend
                   asks Claude for a short natural-language fit summary and a
                   handful of extra skills the keyword matcher might have
                   missed. If no key is set, the app runs fully on the
                   rule-based NLP path and still returns complete results.
"""

import os
import re
import io
import json
import docx
import pdfplumber
from flask import Flask, request, jsonify
from flask_cors import CORS

from skill_data import FLAT_SKILLS, SKILL_CATEGORY

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# ----------------------------------------------------------------------------
# File parsing
# ----------------------------------------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_stream):
    text = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)


def extract_text_from_docx(file_stream):
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(file_storage):
    filename = file_storage.filename
    ext = filename.rsplit(".", 1)[1].lower()
    stream = io.BytesIO(file_storage.read())

    if ext == "pdf":
        return extract_text_from_pdf(stream)
    elif ext == "docx":
        return extract_text_from_docx(stream)
    elif ext == "txt":
        return stream.read().decode("utf-8", errors="ignore")
    return ""


# ----------------------------------------------------------------------------
# Basic resume field extraction (name / email / phone / years of experience)
# ----------------------------------------------------------------------------
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s-]?)?\(?\d{3,4}\)?[\s-]?\d{3}[\s-]?\d{3,4}")
YEARS_RE = re.compile(r"(\d+)\+?\s*(?:years|yrs)\s*(?:of)?\s*experience", re.IGNORECASE)


def extract_contact_info(text):
    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)
    years_match = YEARS_RE.search(text)

    # naive name guess: first non-empty line that looks like a name (<=4 words, no digits/@)
    name = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        words = line.split()
        if 1 <= len(words) <= 4 and not any(ch.isdigit() for ch in line) and "@" not in line:
            name = line
            break

    return {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "years_experience": int(years_match.group(1)) if years_match else None,
    }


# ----------------------------------------------------------------------------
# Skill extraction (rule-based NLP)
# ----------------------------------------------------------------------------
def extract_skills(text):
    """Return {canonical_skill: category} found in text via surface-form matching."""
    lowered = f" {text.lower()} "
    found = {}
    for canonical, variants in FLAT_SKILLS.items():
        for variant in variants:
            pattern = r"(?<![a-zA-Z0-9])" + re.escape(variant.strip().lower()) + r"(?![a-zA-Z0-9])"
            if re.search(pattern, lowered):
                found[canonical] = SKILL_CATEGORY[canonical]
                break
    return found


def compute_match(resume_skills, jd_skills):
    resume_set = set(resume_skills.keys())
    jd_set = set(jd_skills.keys())

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    bonus = sorted(resume_set - jd_set)

    score = round((len(matched) / len(jd_set)) * 100) if jd_set else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "bonus_skills": bonus[:15],  # cap so the UI doesn't overflow
        "score": score,
        "required_count": len(jd_set),
        "matched_count": len(matched),
    }


# ----------------------------------------------------------------------------
# Optional GenAI layer (Anthropic) — gracefully skipped if no API key present
# ----------------------------------------------------------------------------
def genai_enrich(resume_text, jd_text, match_result):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""You are an expert technical recruiter. Given the resume and job
description below, and the keyword-matching results already computed, write:
1. A two-sentence natural-language summary of how well this candidate fits the role.
2. Three short, specific, actionable suggestions to improve the resume for this job.

Respond ONLY in JSON with keys "summary" and "suggestions" (suggestions is a list of strings).

RESUME:
{resume_text[:4000]}

JOB DESCRIPTION:
{jd_text[:2000]}

MATCH SCORE: {match_result['score']}%
MATCHED SKILLS: {', '.join(match_result['matched_skills'])}
MISSING SKILLS: {', '.join(match_result['missing_skills'])}
"""
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        raw = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()
        return json.loads(raw)
    except Exception as e:
        print(f"[genai_enrich] falling back to rule-based summary: {e}")
        return None


def rule_based_summary(match_result):
    score = match_result["score"]
    missing = match_result["missing_skills"]

    if score >= 80:
        summary = "Strong match — this resume covers nearly all the skills this role is asking for."
    elif score >= 50:
        summary = "Partial match — solid overlap, but a few key requirements are missing from the resume."
    else:
        summary = "Weak match — the resume covers only a small portion of the skills this role requires."

    suggestions = []
    if missing:
        suggestions.append(
            f"Add concrete examples of experience with {', '.join(missing[:3])} if you have it."
        )
    suggestions.append("Quantify achievements with numbers (%, $, time saved) wherever possible.")
    suggestions.append("Mirror the exact terminology used in the job description for applicant-tracking systems.")

    return {"summary": summary, "suggestions": suggestions}


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "genai_enabled": bool(os.environ.get("ANTHROPIC_API_KEY"))})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if resume_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(resume_file.filename):
        return jsonify({"error": "Unsupported file type. Use PDF, DOCX, or TXT."}), 400
    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    try:
        resume_text = extract_text(resume_file)
    except Exception as e:
        return jsonify({"error": f"Could not read resume file: {e}"}), 400

    if not resume_text.strip():
        return jsonify({"error": "Could not extract any text from the resume"}), 400

    contact_info = extract_contact_info(resume_text)
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)
    match_result = compute_match(resume_skills, jd_skills)

    insight = genai_enrich(resume_text, job_description, match_result)
    used_genai = insight is not None
    if insight is None:
        insight = rule_based_summary(match_result)

    # group matched/missing skills by category for a nicer UI
    def grouped(skill_list, source_dict):
        groups = {}
        for s in skill_list:
            cat = source_dict.get(s, "Other")
            groups.setdefault(cat, []).append(s)
        return groups

    all_skill_categories = {**resume_skills, **jd_skills}

    return jsonify({
        "contact_info": contact_info,
        "score": match_result["score"],
        "matched_skills": match_result["matched_skills"],
        "missing_skills": match_result["missing_skills"],
        "bonus_skills": match_result["bonus_skills"],
        "matched_grouped": grouped(match_result["matched_skills"], all_skill_categories),
        "missing_grouped": grouped(match_result["missing_skills"], all_skill_categories),
        "required_count": match_result["required_count"],
        "matched_count": match_result["matched_count"],
        "summary": insight["summary"],
        "suggestions": insight["suggestions"],
        "used_genai": used_genai,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
