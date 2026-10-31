"""AI Tools section — the stack students should learn."""

import pandas as pd
import streamlit as st

from data import sample_data as d


def render():
    st.title("AI Tools Section")
    st.write("The tools and technologies used to build modern GenAI applications.")

    df = pd.DataFrame(d.AI_TOOLS, columns=["Tool", "Category", "When to use it"])

    # Optional category filter.
    categories = sorted(df["Category"].unique())
    chosen = st.multiselect("Filter by category", categories, default=categories)
    filtered = df[df["Category"].isin(chosen)] if chosen else df

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.caption(
        "Tip: you do not need all of these at once. Start with Python + Streamlit + an "
        "LLM API, then add LangChain, a vector DB, and deployment as you build RAG apps."
    )
