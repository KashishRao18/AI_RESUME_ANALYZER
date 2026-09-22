# Docket — AI Resume Analyzer

Upload a resume, paste a job description, and get a scored fit verdict:
matched skills, missing skills, bonus skills, and next-step suggestions.

- **Frontend:** React (Vite) + Tailwind CSS — a "case file" themed UI
- **Backend:** Python / Flask — parses PDF/DOCX/TXT resumes and extracts skills
- **NLP:** rule-based skill-taxonomy matcher (works fully offline)
- **GenAI (optional):** if you set `ANTHROPIC_API_KEY`, the backend asks Claude
  for a natural-language fit summary and tailored suggestions. Without a key,
  everything still works using the rule-based matcher.

## Project structure

```
ai-resume-analyzer/
├── backend/
│   ├── app.py            # Flask app + API routes
│   ├── skill_data.py      # skill taxonomy used by the extractor
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   └── components/
    ├── index.html
    └── package.json
```

## Running it

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# optional — enables Claude-generated summaries
cp .env.example .env            # then fill in ANTHROPIC_API_KEY
export $(cat .env | xargs)      # or use python-dotenv / your shell's method

python app.py
```
The API runs at `http://localhost:5000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```
The app runs at `http://localhost:5173` and proxies `/api/*` calls to the
Flask backend automatically (see `vite.config.js`).

Open `http://localhost:5173`, upload a resume (PDF, DOCX, or TXT), paste a
job description, and click **Open review**.

## How matching works

`backend/skill_data.py` defines ~70 skills across Languages, Frontend,
Backend, Data/ML/AI, Cloud/DevOps, Databases, and Soft Skills, each with
common surface forms (e.g. "js", "javascript", "react.js"). The resume and
job description are both scanned for these skills; the match score is
`matched required skills / total required skills`. Add more skills or
synonyms directly in `skill_data.py` — no other code changes needed.

## Extending it

- Swap the rule-based extractor for spaCy NER if you want fuzzier matching.
- The GenAI hook in `app.py` (`genai_enrich`) is a good place to add resume
  rewriting, cover-letter drafting, or interview-question generation.
- Deploy the backend anywhere Flask runs (Render, Railway, Fly.io) and the
  frontend as a static build (`npm run build`) on Vercel/Netlify — just point
  `VITE_API_BASE` at your backend URL.
