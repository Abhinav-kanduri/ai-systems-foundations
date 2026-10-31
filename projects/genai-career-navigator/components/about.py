"""About section."""

import streamlit as st

from data import sample_data as d


def render():
    st.title("About")
    st.write(
        "The **GenAI Career Navigator** is an educational dashboard that guides students "
        "and career switchers from beginner to job-ready in Generative AI — covering "
        "roadmaps, skills, projects, RAG, tools, interviews, resumes, and job search."
    )

    st.markdown("**Built with:** Python · Streamlit · Pandas · Plotly")

    st.divider()
    st.markdown(f"**Published by {d.AUTHOR}**")
    st.markdown(f"LinkedIn: {d.LINKEDIN_URL}")
