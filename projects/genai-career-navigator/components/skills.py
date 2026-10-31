"""Skill Roadmap section — skill tree with difficulty filter and readiness chart."""

import pandas as pd
import plotly.express as px
import streamlit as st

from data import sample_data as d


def render():
    st.title("Skill Roadmap")
    st.write("A structured skill tree from foundations to advanced GenAI skills.")

    # Build a dataframe from the skill tree for filtering/among charts.
    df = pd.DataFrame(
        d.SKILL_TREE,
        columns=["Skill", "Definition", "Why it matters", "Tools", "Mini project", "Level"],
    )

    # --- Difficulty filter ----------------------------------------------
    levels = st.multiselect(
        "Filter by difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        default=["Beginner", "Intermediate", "Advanced"],
    )
    filtered = df[df["Level"].isin(levels)] if levels else df

    # --- Skill count by level chart -------------------------------------
    counts = filtered["Level"].value_counts().reindex(
        ["Beginner", "Intermediate", "Advanced"]
    ).fillna(0).reset_index()
    counts.columns = ["Level", "Count"]
    fig = px.bar(counts, x="Level", y="Count", text="Count", title="Skills by difficulty")
    st.plotly_chart(fig, use_container_width=True)

    # --- Skill details --------------------------------------------------
    st.markdown("### Skill details")
    for _, row in filtered.iterrows():
        with st.expander(f"{row['Skill']}  ·  {row['Level']}"):
            st.write(f"**Definition:** {row['Definition']}")
            st.write(f"**Why it matters:** {row['Why it matters']}")
            st.write("**Tools:** " + ", ".join(row["Tools"]))
            st.write(f"**Mini project idea:** {row['Mini project']}")
