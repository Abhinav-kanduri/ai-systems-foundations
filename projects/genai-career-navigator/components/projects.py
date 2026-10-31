"""Project Portfolio Builder section — filterable project ideas."""

import pandas as pd
import streamlit as st

from components import ui
from data import sample_data as d


def render():
    st.title("Project Portfolio Builder")
    st.write("Production-style GenAI project ideas you can build and put on your resume.")

    # --- Difficulty filter ----------------------------------------------
    levels = st.multiselect(
        "Filter by difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        default=["Beginner", "Intermediate", "Advanced"],
    )
    projects = [p for p in d.PROJECTS if p["difficulty"] in levels] if levels else d.PROJECTS

    # --- Overview table -------------------------------------------------
    overview = pd.DataFrame(
        [
            {
                "Project": p["name"],
                "Difficulty": p["difficulty"],
                "Resume value": p["resume_value"],
                "Tech stack": ", ".join(p["tech"]),
            }
            for p in projects
        ]
    )
    st.dataframe(overview, use_container_width=True, hide_index=True)

    # --- Detail view ----------------------------------------------------
    st.markdown("### Project details")
    names = [p["name"] for p in projects]
    if not names:
        st.warning("No projects match the selected filters.")
        return

    selected = st.selectbox("Select a project", names)
    p = next(x for x in projects if x["name"] == selected)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Difficulty:** {p['difficulty']}")
        st.markdown(f"**Resume value:** {p['resume_value']}")
        st.markdown(f"**Problem:** {p['problem']}")
        st.markdown(f"**Target users:** {p['persona']}")
        st.markdown("**Features**")
        st.markdown("\n".join(f"- {f}" for f in p["features"]))
    with c2:
        st.markdown("**Tech stack:** " + ", ".join(p["tech"]))
        st.markdown(f"**Vector database:** {p['vector_db']}")
        st.markdown(f"**Deployment:** {p['deploy']}")
        st.markdown("**Evaluation metrics**")
        st.markdown("\n".join(f"- {e}" for e in p["eval"]))

    st.markdown("**Architecture / data flow**")
    # The architecture strings use arrow separators; turn them into a step flow.
    steps = [s for s in p["architecture"].replace(".", "").split("→")]
    if len(steps) > 1:
        ui.flow(steps)
    else:
        st.code(p["architecture"])

    st.markdown("**Resume bullets**")
    for b in p["bullets"]:
        st.markdown(f"- {b}")

    with st.expander("Suggested GitHub README structure"):
        st.markdown("\n".join(f"- {s}" for s in p["readme"]))
