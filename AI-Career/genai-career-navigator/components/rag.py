"""RAG Learning section — explains Retrieval-Augmented Generation."""

import pandas as pd
import streamlit as st

from components import ui
from data import sample_data as d


def render():
    st.title("RAG Learning Section")

    st.subheader("What is RAG?")
    st.write(
        "RAG stands for **Retrieval-Augmented Generation**. It lets an LLM answer using "
        "your own documents instead of relying only on what it learned during training. "
        "This makes answers more accurate, up to date, and grounded in real sources."
    )

    # --- Flow ------------------------------------------------------------
    st.subheader("The RAG flow")
    st.caption("How a question becomes a grounded answer, step by step.")
    ui.flow(d.RAG_FLOW, numbered=True)

    # --- Components table ------------------------------------------------
    st.subheader("RAG components")
    comp_df = pd.DataFrame(d.RAG_COMPONENTS, columns=["Component", "Purpose"])
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # --- Key concepts ----------------------------------------------------
    st.subheader("Key concepts explained")
    for concept, explanation in d.RAG_CONCEPTS.items():
        with st.expander(concept):
            st.write(explanation)

    st.info(
        "RAG is one of the most in-demand GenAI skills for freshers — building one "
        "RAG chatbot dramatically strengthens your portfolio."
    )
