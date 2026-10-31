"""Interview Preparation section — senior / high-signal Q&A by topic."""

import streamlit as st

from components import ui
from data import sample_data as d


def render():
    st.title("Interview Preparation")
    st.write(
        "Senior-level questions focused on system design, modern GenAI engineering, and "
        "current trends — agentic systems, retrieval infra, LLMOps, evaluation, and "
        "production cost/latency tradeoffs. Each answer is the level you should aim for."
    )

    topic = st.selectbox("Choose a topic", list(d.INTERVIEW_QA.keys()))

    # Anchor the system-design discussion with a reference architecture.
    if topic == "LLM Systems Design":
        st.markdown("#### Reference architecture to reason from")
        st.caption("A production RAG assistant, split into indexing and serving planes.")
        for lane_title, steps in d.INTERVIEW_SYSTEM_DESIGN.items():
            ui.lane(lane_title, steps, numbered=True)

    for question, answer, key_points in d.INTERVIEW_QA[topic]:
        with st.expander(question):
            st.markdown("**How a strong candidate answers**")
            st.success(answer)
            st.markdown("**Key points to hit:** " + ", ".join(key_points))
