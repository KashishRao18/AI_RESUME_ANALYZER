# -----------------------------------------------------------------------------
# skill_data.py
# A hand-curated skill taxonomy used by the rule-based / NLP extractor.
# Each canonical skill maps to a list of surface forms (synonyms, abbreviations,
# casing variants) that the extractor will look for in resume / job description
# text. Grouped by category purely for display purposes.
# -----------------------------------------------------------------------------

SKILL_TAXONOMY = {
    "Languages": {
        "Python": ["python", "python3"],
        "JavaScript": ["javascript", "js", "es6", "ecmascript"],
        "TypeScript": ["typescript", "ts"],
        "Java": ["java"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "csharp", ".net"],
        "Go": ["golang", "go lang", " go "],
        "Rust": ["rust"],
        "SQL": ["sql", "mysql", "postgresql", "t-sql", "pl/sql"],
        "R": [" r programming", "r language"],
        "Swift": ["swift"],
        "Kotlin": ["kotlin"],
        "PHP": ["php"],
        "Ruby": ["ruby"],
        "Scala": ["scala"],
    },
    "Frontend": {
        "React": ["react", "react.js", "reactjs"],
        "Vue.js": ["vue", "vue.js", "vuejs"],
        "Angular": ["angular", "angularjs"],
        "HTML/CSS": ["html", "css", "html5", "css3"],
        "Tailwind CSS": ["tailwind", "tailwindcss"],
        "Redux": ["redux"],
        "Next.js": ["next.js", "nextjs"],
        "Sass": ["sass", "scss"],
    },
    "Backend": {
        "Flask": ["flask"],
        "Django": ["django"],
        "FastAPI": ["fastapi"],
        "Node.js": ["node.js", "nodejs", "node js"],
        "Express.js": ["express.js", "expressjs", "express"],
        "Spring Boot": ["spring boot", "spring"],
        "REST APIs": ["rest api", "restful", "rest apis"],
        "GraphQL": ["graphql"],
        "Microservices": ["microservices", "microservice architecture"],
    },
    "Data / ML / AI": {
        "Machine Learning": ["machine learning", "ml "],
        "Deep Learning": ["deep learning", "dl "],
        "NLP": ["nlp", "natural language processing"],
        "Computer Vision": ["computer vision", "cv "],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "scikit-learn": ["scikit-learn", "sklearn"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Generative AI": ["generative ai", "genai", "gen ai", "llm", "large language model"],
        "Data Analysis": ["data analysis", "data analytics"],
        "Data Visualization": ["data visualization", "tableau", "power bi"],
        "Spark": ["apache spark", "pyspark", " spark"],
    },
    "Cloud / DevOps": {
        "AWS": ["aws", "amazon web services"],
        "Azure": ["azure", "microsoft azure"],
        "GCP": ["gcp", "google cloud"],
        "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
        "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
        "Terraform": ["terraform"],
        "Jenkins": ["jenkins"],
        "Linux": ["linux", "unix"],
        "Git": ["git", "github", "gitlab", "version control"],
    },
    "Databases": {
        "MongoDB": ["mongodb", "mongo db"],
        "PostgreSQL": ["postgresql", "postgres"],
        "MySQL": ["mysql"],
        "Redis": ["redis"],
        "Elasticsearch": ["elasticsearch"],
        "Firebase": ["firebase"],
    },
    "Soft Skills": {
        "Communication": ["communication skills", "communication"],
        "Leadership": ["leadership", "team lead", "led a team"],
        "Problem Solving": ["problem solving", "problem-solving"],
        "Teamwork": ["teamwork", "collaboration", "cross-functional"],
        "Project Management": ["project management", "agile", "scrum", "kanban"],
        "Time Management": ["time management"],
        "Adaptability": ["adaptability", "fast-paced environment"],
    },
}

# Flatten to {canonical_skill: [surface forms...]} and {canonical_skill: category}
FLAT_SKILLS = {}
SKILL_CATEGORY = {}
for category, skills in SKILL_TAXONOMY.items():
    for canonical, variants in skills.items():
        FLAT_SKILLS[canonical] = variants
        SKILL_CATEGORY[canonical] = category
