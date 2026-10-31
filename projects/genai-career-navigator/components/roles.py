"""GenAI Role Explorer section — role cards."""

import streamlit as st

from data import sample_data as d


def render():
    st.title("GenAI Role Explorer")
    st.write("Browse GenAI roles and understand what each one needs.")

    # Let the user filter to one role or view all as cards.
    choice = st.selectbox("Choose a role", ["All roles"] + list(d.GENAI_ROLES.keys()))

    roles = d.GENAI_ROLES if choice == "All roles" else {choice: d.GENAI_ROLES[choice]}

    for name, info in roles.items():
        with st.expander(f"{name}", expanded=(choice != "All roles")):
            st.write(f"**What the role does:** {info['does']}")
            st.write(f"**Best for:** {info['best_for']}")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Required skills**")
                st.markdown("\n".join(f"- {s}" for s in info["skills"]))
                st.markdown("**Example projects**")
                st.markdown("\n".join(f"- {p}" for p in info["projects"]))
            with c2:
                st.markdown("**Tools & technologies**")
                st.markdown("\n".join(f"- {t}" for t in info["tools"]))
                st.markdown("**Interview topics**")
                st.markdown("\n".join(f"- {t}" for t in info["interview"]))

            st.markdown("**Resume keywords:** " + ", ".join(info["keywords"]))
            st.info(f"**Preparation path:** {info['prep']}")
