"""Progress Tracker section — sliders + readiness score."""

import pandas as pd
import plotly.express as px
import streamlit as st

from data import sample_data as d


def render():
    st.title("Progress Tracker")
    st.write("Move the sliders to reflect where you are today and see your readiness score.")

    # One slider per area; defaults come from sample data.
    scores = {}
    cols = st.columns(2)
    for i, (area, default) in enumerate(d.PROGRESS_AREAS.items()):
        with cols[i % 2]:
            scores[area] = st.slider(area, 0, 100, default, key=f"prog_{area}")

    df = pd.DataFrame({"Area": list(scores.keys()), "Progress": list(scores.values())})

    # Line chart of progress across areas.
    fig = px.line(
        df, x="Area", y="Progress", markers=True, title="Your preparation progress",
    )
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    # Overall readiness score + recommendation.
    average = df["Progress"].mean()
    st.metric("Overall Readiness Score", f"{average:.1f}%")

    if average < 40:
        st.warning("Focus on the basics and complete at least one working project.")
    elif average < 70:
        st.info("Good progress. Strengthen RAG, deployment, and GitHub documentation.")
    else:
        st.success("Strong readiness. Start applying seriously and prepare for interviews.")
