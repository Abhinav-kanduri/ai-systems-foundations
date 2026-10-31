# Presentation Script — GenAI Career Navigator

A ready-to-speak script for demoing the dashboard end-to-end to students
(about 10–15 minutes). Speak the **quoted** lines; the notes tell you what to click.

---

## 1. Opening (30 sec)
> "Today I'll show you a Streamlit app I built called the **GenAI Career Navigator**.
> It's an interactive dashboard that takes a complete beginner and walks them all the
> way to a job-ready Generative AI professional — skills, roadmap, projects, interviews,
> and jobs. Let's walk through it."

*Have the app already running (`streamlit run app.py`). Point to the sidebar.*

## 2. Home Dashboard (1 min)
*Click **Home Dashboard**.*
> "The home page explains what Generative AI is and why it's worth learning. Up here are
> quick metrics — target roles, a 90-day timeline, skill areas, and projects. Below, these
> cards preview the whole journey, and this chart shows where to focus your energy."

## 3. Career Path Explorer (1.5 min)
*Click **Career Path Explorer**. Change the dropdown to two different backgrounds.*
> "This is the personalization piece. Whether you're a fresher, an IT professional, or
> coming from a non-technical background, it gives you a tailored path — the skills, tools,
> projects, target roles, and a 30/60/90-day plan for exactly your starting point."

## 4. GenAI Role Explorer (1.5 min)
*Click **GenAI Role Explorer**. Expand one or two role cards.*
> "Here you can explore real GenAI roles — AI Engineer, LLM Engineer, RAG Engineer,
> Prompt Engineer, and more. Each card shows what the role does, the skills and tools,
> example projects, interview topics, resume keywords, and how to prepare."

## 5. Skill Roadmap (1 min)
*Click **Skill Roadmap**. Use the difficulty filter.*
> "This is the full skill tree, from Python all the way to AI agents and evaluation. You
> can filter by difficulty, and each skill has a definition, why it matters, the tools, and
> a mini-project idea so you learn by building."

## 6. Learning Roadmap (1 min)
*Click **Learning Roadmap**. Switch between 30/60/90-day phases.*
> "This turns everything into a week-by-week plan across three phases. Each week has
> topics, hands-on tasks, a project milestone, and an expected outcome."

## 7. Project Portfolio Builder (1.5 min)
*Click **Project Portfolio Builder**. Filter by difficulty, then open a project.*
> "Projects are what actually get you hired. Each idea comes with a problem statement,
> features, architecture, tech stack, evaluation metrics, a deployment plan, and even
> ready-to-use resume bullets and a README structure."

## 8. RAG Learning (1 min)
*Click **RAG Learning**.*
> "RAG — Retrieval-Augmented Generation — is the most in-demand GenAI skill right now.
> This section explains the flow, the components, and key concepts like chunking,
> embeddings, and reducing hallucinations."

## 9. AI Tools (30 sec)
*Click **AI Tools**.*
> "A quick reference to the tools you'll use and when to use each one — from Python and
> Streamlit to LangChain, vector databases, and cloud deployment."

## 10. Interview Preparation (1 min)
*Click **Interview Preparation**. Pick a topic and expand a question.*
> "For interviews, every question shows a beginner answer, a strong answer, and the key
> points to remember — across Python, ML, LLMs, RAG, system design, and behavioral."

## 11. Resume & LinkedIn (45 sec)
*Click **Resume & LinkedIn**. Show the tabs.*
> "Copy-ready resume summaries and bullets, LinkedIn headline and About examples, plus a
> GitHub and portfolio checklist."

## 12. Job Search Strategy (45 sec)
*Click **Job Search Strategy**.*
> "Target job titles, Boolean search strings, a weekly application plan, and a recruiter
> outreach template — everything to run an organized job search."

## 13. Future AI Opportunities (30 sec)
*Click **Future AI Opportunities**.*
> "This looks ahead — agents, multimodal AI, automation, governance — and maps each trend
> to the skills you'd learn to be ready for it."

## 14. Progress Tracker (1 min)
*Click **Progress Tracker**. Move a few sliders live.*
> "Students can track themselves here. As I move these sliders, the app recalculates an
> overall readiness score and gives a recommendation on what to focus on next."

## 15. Student Action Plan (1 min)
*Click **Student Action Plan**. Fill the form and submit.*
> "Finally, the personalized planner. A student enters their background, level, target role,
> and timeline, and the app generates a custom plan — recommended role, skills, projects,
> a 30-day plan, resume advice, and job-search keywords."

## 16. Closing (30 sec)
*Click **Final Recommendations**, then **About**.*
> "It wraps up with clear next steps and a 7-day starter plan. The whole app is built with
> Python, Streamlit, Pandas, and Plotly, and it's modular so it's easy to extend. Thank you!"

---

## Technical talking points (if asked)
- **Stack:** Python, Streamlit (UI), Pandas (tables), Plotly (charts).
- **Architecture:** `app.py` handles sidebar navigation and routes to one `render()`
  function per section in `components/`; all content lives in `data/sample_data.py`.
- **No database needed:** everything uses in-app sample data, so it runs anywhere.
- **Future scope:** connect LLM APIs for personalized plans and resume feedback, add
  login and database-backed progress, and embed a live RAG chatbot.

---
Published by Abhinav Konduri
LinkedIn: linkedin.com/in/abhinav-kanduri-a943b9353
