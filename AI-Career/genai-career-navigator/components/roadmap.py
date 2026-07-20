"""Learning Roadmap section — 30/60/90-day weekly plans."""

import pandas as pd
import streamlit as st

from components import ui
from data import sample_data as d


def render():
    st.title("Learning Roadmap")
    st.write("A 90-day plan broken into 30 / 60 / 90-day phases with weekly milestones.")

    # --- Phase overview cards -------------------------------------------
    st.markdown("### How the 90 days flow")
    ui.phase_cards(
        [
            ("30 Days", "Foundations", "Python, ML basics, and Git."),
            ("60 Days", "LLM Apps", "LLM APIs, Streamlit, and embeddings."),
            ("90 Days", "RAG + Deploy", "RAG, deployment, portfolio, and jobs."),
        ]
    )

    phase = st.radio(
        "Choose a phase", list(d.WEEKLY_ROADMAP.keys()), horizontal=True
    )
    weeks = d.WEEKLY_ROADMAP[phase]

    # Table view of the selected phase.
    df = pd.DataFrame(
        weeks, columns=["Week", "Topics", "Hands-on tasks", "Project milestone", "Expected outcome"]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Expandable weekly sections for a walkthrough during presentations.
    st.markdown("### Week-by-week")
    for week, topics, tasks, milestone, outcome in weeks:
        with st.expander(f"Week {week}: {topics}"):
            st.write(f"**Hands-on tasks:** {tasks}")
            st.write(f"**Project milestone:** {milestone}")
            st.write(f"**Expected outcome:** {outcome}")

    st.success(
        "By the end of 90 days you should have 3 portfolio projects, a deployed app, "
        "and be ready to apply for internships and junior AI roles."
    )
