"""Job Search Strategy section."""

import pandas as pd
import streamlit as st

from data import sample_data as d


def render():
    st.title("Job Search Strategy")

    st.subheader("Target job titles")
    # Show titles as a compact wrapped list.
    st.write(" · ".join(d.JOB_TITLES))

    st.subheader("Boolean search strings")
    for s in d.BOOLEAN_SEARCHES:
        st.code(s)

    st.subheader("Weekly application plan")
    plan_df = pd.DataFrame(d.WEEKLY_JOB_PLAN, columns=["Activity", "Weekly target"])
    st.table(plan_df)

    st.subheader("Recruiter message template")
    st.info(d.RECRUITER_MESSAGE)

    st.subheader("Networking strategy")
    for t in d.NETWORKING_TIPS:
        st.markdown(f"- {t}")
