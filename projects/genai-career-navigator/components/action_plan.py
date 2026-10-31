"""Student Action Plan section — form that generates a personalized plan."""

import streamlit as st

from data import sample_data as d


def render():
    st.title("Student Action Plan")
    st.write("Fill in your details and get a personalized starting plan.")

    with st.form("action_plan_form"):
        name = st.text_input("Your name", "")
        background = st.selectbox("Current background", list(d.CAREER_PATHS.keys()))
        level = st.select_slider(
            "Current skill level", ["Beginner", "Intermediate", "Advanced"], value="Beginner"
        )
        target_role = st.selectbox("Target AI role", list(d.GENAI_ROLES.keys()))
        timeline = st.selectbox("Timeline", ["30 Days", "60 Days", "90 Days", "6 Months"])
        area = st.selectbox(
            "Preferred project area",
            ["RAG / Chatbots", "AI Agents", "AI Automation", "AI Analytics", "AI Product"],
        )
        submitted = st.form_submit_button("Generate my action plan")

    if not submitted:
        return

    path = d.CAREER_PATHS[background]
    role = d.GENAI_ROLES[target_role]
    greeting = f"Here is your plan, {name}!" if name.strip() else "Here is your plan!"

    st.success(greeting)

    st.markdown(f"### Recommended role: {target_role}")
    st.write(role["does"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Skills to learn**")
        # Combine background + role skills, keeping order and removing duplicates.
        skills = list(dict.fromkeys(path["skills"] + role["skills"]))
        st.markdown("\n".join(f"- {s}" for s in skills))
    with c2:
        st.markdown("**Projects to build**")
        projects = list(dict.fromkeys(path["projects"] + role["projects"]))
        st.markdown("\n".join(f"- {p}" for p in projects))

    # Pick the roadmap phase closest to the chosen timeline.
    phase = timeline if timeline in path["roadmap"] else "90 Days"
    st.markdown(f"### 30-day action plan ({level} · target {timeline})")
    st.info(path["roadmap"].get("30 Days", ""))

    st.markdown("**Resume improvement advice**")
    st.write(
        "Add project-based bullets that name your tools and impact. Example: "
        f"\"{role['keywords'][0]} project using {', '.join(role['tools'][:2])}.\""
    )

    st.markdown("**Job search keywords**")
    st.write(", ".join(role["keywords"]))

    st.caption(f"Preferred focus area noted: **{area}** — prioritize projects there first.")
