"""Future AI Opportunities section."""

import streamlit as st

from data import sample_data as d


def render():
    st.title("Future AI Opportunities")
    st.write(
        "AI is evolving fast. These are the trends creating tomorrow's roles — and the "
        "skills that map to each one."
    )

    for name, desc, skills in d.FUTURE_TRENDS:
        with st.expander(f"{name}"):
            st.write(desc)
            st.markdown("**Matching skills to learn:** " + ", ".join(skills))

    st.success(
        "Domain-specific AI (finance, healthcare, education, enterprise) will need people "
        "who combine AI skills with domain knowledge — a great edge for career switchers."
    )
