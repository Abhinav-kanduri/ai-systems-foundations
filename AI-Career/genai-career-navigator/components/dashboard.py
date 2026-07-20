"""Home / Introduction dashboard section."""

import pandas as pd
import plotly.express as px
import streamlit as st

from components import ui
from data import sample_data as d


def render():
    # --- Title and intro -------------------------------------------------
    st.title("GenAI Career Navigator")
    st.subheader("Build your future career in Generative AI")

    st.write(
        "Generative AI creates new text, code, images, and more using large language "
        "models (LLMs). It is one of the fastest-growing areas in tech, opening roles "
        "in AI engineering, RAG systems, AI agents, automation, and AI product work."
    )

    # --- The big picture: end-to-end career path -------------------------
    st.markdown("### The GenAI career path at a glance")
    st.caption("Follow this path step by step — each stage builds on the previous one.")
    ui.flow(
        [
            "Python", "ML Basics", "Prompt Engineering", "LLM APIs", "Embeddings",
            "Vector Databases", "RAG", "AI Agents", "Deployment", "Portfolio",
            "Job Applications",
        ]
    )

    with st.expander("Why should students learn Generative AI?"):
        st.markdown(
            "- **High demand & pay:** companies need people who can build with LLMs.\n"
            "- **Low barrier to start:** you can build real apps with Python + an API.\n"
            "- **Portfolio-friendly:** a few strong projects can land internships.\n"
            "- **Future-proof:** AI skills apply across almost every industry."
        )

    st.info(
        "**Goal of this dashboard:** guide you step by step from beginner to a "
        "job-ready GenAI professional — skills, roadmap, projects, interviews, and jobs."
    )

    # --- Top metrics -----------------------------------------------------
    cols = st.columns(len(d.HOME_METRICS))
    for col, (label, value) in zip(cols, d.HOME_METRICS):
        col.metric(label, value)

    # --- Summary cards ---------------------------------------------------
    st.markdown("### Explore the journey")
    card_cols = st.columns(3)
    for i, (title, desc) in enumerate(d.SUMMARY_CARDS):
        with card_cols[i % 3]:
            st.markdown(f"**{title}**")
            st.caption(desc)

    # --- Preparation-areas chart ----------------------------------------
    st.markdown("### Career preparation areas")
    prep_df = pd.DataFrame(
        {"Area": list(d.PREP_AREAS.keys()), "Focus %": list(d.PREP_AREAS.values())}
    )
    fig = px.bar(
        prep_df, x="Area", y="Focus %", text="Focus %",
        title="Where to focus your energy on the way to a GenAI role",
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
