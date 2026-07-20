"""Career Path Explorer section — guidance per background."""

import streamlit as st

from data import sample_data as d


def render():
    st.title("Career Path Explorer")
    st.write("Pick your current background to see a tailored path into Generative AI.")

    # Dropdown to choose a background (keeps the page compact).
    background = st.selectbox("I am currently a...", list(d.CAREER_PATHS.keys()))
    info = d.CAREER_PATHS[background]

    st.markdown(f"### Path for: {background}")
    st.caption(f"**Starting from:** {info['starting_from']}")
    st.success(f"**Best AI career path:** {info['best_path']}")

    # Two columns of lists for a clean layout.
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Skills to learn**")
        for s in info["skills"]:
            st.markdown(f"- {s}")
        st.markdown("**Projects to build**")
        for p in info["projects"]:
            st.markdown(f"- {p}")
    with c2:
        st.markdown("**Tools to learn**")
        for t in info["tools"]:
            st.markdown(f"- {t}")
        st.markdown("**Roles to target**")
        for r in info["roles"]:
            st.markdown(f"- {r}")

    # 30/60/90-day roadmap for this background.
    st.markdown("### 30 / 60 / 90-day roadmap")
    r1, r2, r3 = st.columns(3)
    for col, phase in zip((r1, r2, r3), ("30 Days", "60 Days", "90 Days")):
        with col:
            st.markdown(f"**{phase}**")
            st.write(info["roadmap"][phase])
