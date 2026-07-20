"""Final Recommendations section."""

import streamlit as st


def render():
    st.title("Final Recommendations")

    st.subheader("What to do next")
    st.markdown(
        "1. Build strong Python basics.\n"
        "2. Learn prompt engineering and LLM APIs.\n"
        "3. Build one Streamlit GenAI app.\n"
        "4. Build one RAG chatbot with a vector database.\n"
        "5. Upload all projects to GitHub with clean READMEs.\n"
        "6. Update your LinkedIn headline and post project updates.\n"
        "7. Apply for AI intern, GenAI intern, and junior AI roles."
    )

    st.subheader("Your next 7 days")
    seven_day = [
        "Day 1: Set up Python, Git, and a GitHub account.",
        "Day 2: Practice calling an LLM API from Python.",
        "Day 3: Build a small Streamlit app using the API.",
        "Day 4: Learn embeddings and semantic search.",
        "Day 5: Start a PDF RAG chatbot project.",
        "Day 6: Write a clean README for it.",
        "Day 7: Post your progress on LinkedIn.",
    ]
    for item in seven_day:
        st.markdown(f"- {item}")

    st.success(
        "In 90 days you can have 3 GenAI projects, a portfolio, and a resume with real "
        "project experience — enough to start applying with confidence. Keep building, "
        "keep shipping, and stay consistent. You've got this!"
    )
