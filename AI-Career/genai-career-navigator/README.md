# GenAI Career Navigator Dashboard

An interactive, presentation-ready Streamlit app that guides students, freshers,
and career switchers through a complete path into a Generative AI career —
roadmaps, skills, projects, RAG, tools, interviews, resume/LinkedIn, job search,
future trends, a progress tracker, and a personalized action plan.

## Features

- Sidebar navigation across 16 sections
- Dashboards, charts (Plotly), tables (pandas), cards, tabs, expanders
- Career Path Explorer for different backgrounds (fresher, IT, non-IT, etc.)
- GenAI Role Explorer with role cards
- 30 / 60 / 90-day learning roadmap
- Project Portfolio Builder with difficulty filters
- Interactive Progress Tracker with a readiness score
- Personalized Student Action Plan form
- Sample data baked in — no database required

## Project structure

```
genai-career-navigator/
├── app.py                     # Sidebar navigation + routing
├── requirements.txt
├── README.md
├── PRESENTATION_SCRIPT.md     # End-to-end demo script for a classroom
├── data/
│   └── sample_data.py         # All content/data in one place
└── components/
    ├── dashboard.py
    ├── career_paths.py
    ├── roles.py
    ├── skills.py
    ├── roadmap.py
    ├── projects.py
    ├── rag.py
    ├── tools.py
    ├── resume_linkedin.py
    ├── interview.py
    ├── job_search.py
    ├── future.py
    ├── progress_tracker.py
    ├── action_plan.py
    └── recommendations.py
```

## Setup and run

From inside the `genai-career-navigator/` folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

If `streamlit` is not found, use the module form:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Do **not** run `python app.py` — Streamlit apps must be launched with
`streamlit run app.py`.

## Verify the install

```bash
python -c "import streamlit, pandas, plotly; print('ok')"
```

## Future improvements

- Connect LLM APIs to generate personalized plans and resume feedback
- Add user login and database-backed progress storage
- Add a live PDF RAG chatbot inside the dashboard
- Deploy on Streamlit Community Cloud and share the live link

---
Published by Abhinav Konduri
LinkedIn: linkedin.com/in/abhinav-kanduri-a943b9353
