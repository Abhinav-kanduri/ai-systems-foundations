"""Resume & LinkedIn Readiness section."""

import streamlit as st

from data import sample_data as d


def render():
    st.title("Resume & LinkedIn Readiness")

    tab1, tab2, tab3 = st.tabs(["Resume", "LinkedIn", "GitHub & Portfolio"])

    # --- Resume ----------------------------------------------------------
    with tab1:
        st.subheader("Resume summary (copy-ready)")
        st.success(d.RESUME_SUMMARY)

        st.subheader("Project-based resume bullets")
        for b in d.RESUME_BULLETS:
            st.markdown(f"- {b}")
        st.caption("Tip: add metrics where you can (accuracy, time saved, users).")

    # --- LinkedIn --------------------------------------------------------
    with tab2:
        st.subheader("LinkedIn headline examples")
        for h in d.LINKEDIN_HEADLINES:
            st.info(h)

        st.subheader("LinkedIn About section (example)")
        st.write(d.LINKEDIN_ABOUT)

    # --- GitHub & Portfolio ---------------------------------------------
    with tab3:
        st.subheader("GitHub profile tips")
        for t in d.GITHUB_TIPS:
            st.markdown(f"- {t}")

        st.subheader("Portfolio checklist")
        for item in d.PORTFOLIO_CHECKLIST:
            st.checkbox(item, key=f"portfolio_{item}")
