"""
GenAI Career Navigator Dashboard
================================

An interactive, presentation-ready Streamlit app that guides students and career
switchers into a Generative AI career.

Run it with:
    streamlit run app.py

Each section lives in its own module under `components/`, and all content data
lives in `data/sample_data.py`, so the app is easy to extend.
"""

import streamlit as st

# Import each section module. Every module exposes a `render()` function.
from components import (
    about,
    action_plan,
    career_paths,
    dashboard,
    future,
    interview,
    job_search,
    progress_tracker,
    projects,
    rag,
    recommendations,
    resume_linkedin,
    roadmap,
    roles,
    skills,
    tools,
    ui,
)
from data import sample_data as d

# --- Page configuration --------------------------------------------------
st.set_page_config(
    page_title="GenAI Career Navigator",
    page_icon="",
    layout="wide",
)

# Global styling applied to every page.
ui.inject_css()

# --- Sidebar navigation --------------------------------------------------
# Map a friendly menu label to the render function for that section.
PAGES = {
    "Home Dashboard": dashboard.render,
    "Career Path Explorer": career_paths.render,
    "GenAI Role Explorer": roles.render,
    "Skill Roadmap": skills.render,
    "Learning Roadmap": roadmap.render,
    "Project Portfolio Builder": projects.render,
    "RAG Learning": rag.render,
    "AI Tools": tools.render,
    "Resume & LinkedIn": resume_linkedin.render,
    "Interview Preparation": interview.render,
    "Job Search Strategy": job_search.render,
    "Future AI Opportunities": future.render,
    "Progress Tracker": progress_tracker.render,
    "Student Action Plan": action_plan.render,
    "Final Recommendations": recommendations.render,
    "About": about.render,
}

st.sidebar.title("GenAI Career Navigator")
st.sidebar.caption("Build your future career in Generative AI")

choice = st.sidebar.radio("Go to section", list(PAGES.keys()))

st.sidebar.divider()
st.sidebar.markdown(f"**Published by {d.AUTHOR}**")
st.sidebar.caption(d.LINKEDIN_URL)

# --- Render the selected section ----------------------------------------
PAGES[choice]()
