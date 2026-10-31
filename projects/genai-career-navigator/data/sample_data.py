"""
Central data module for the GenAI Career Navigator dashboard.

All content shown in the app lives here so the UI components stay clean and the
data is easy to extend. Nothing here touches a database — it is plain Python
dictionaries and lists that the components render.
"""

# ---------------------------------------------------------------------------
# Home dashboard summary cards + top-level metrics
# ---------------------------------------------------------------------------

SUMMARY_CARDS = [
    ("Freshers Path", "Start from Python and grow into a job-ready GenAI developer."),
    ("IT Professionals Path", "Reuse your engineering base and pivot into AI/LLM roles."),
    ("Non-IT Path", "Move into AI-enabled roles using tools, prompts, and automation."),
    ("High-Paying AI Skills", "RAG, agents, LLM APIs, evaluation, and deployment."),
    ("Future AI Roles", "AI Engineer, LLM Engineer, RAG Engineer, AI PM, and more."),
    ("Project Portfolio", "Build 3+ production-style GenAI projects for your resume."),
]

HOME_METRICS = [
    ("Target Roles", "10+"),
    ("Learning Duration", "90 Days"),
    ("Skill Areas", "8"),
    ("Portfolio Projects", "9"),
]

# Radar/bar of the preparation areas shown on the home dashboard.
PREP_AREAS = {
    "AI Foundations": 70,
    "Python": 80,
    "LLMs": 65,
    "RAG": 55,
    "AI Agents": 45,
    "Cloud": 50,
    "Projects": 60,
    "Interview Prep": 40,
}

# ---------------------------------------------------------------------------
# Career Path Explorer — one entry per background
# ---------------------------------------------------------------------------

CAREER_PATHS = {
    "Fresher": {
        "starting_from": "No professional experience; learning fundamentals.",
        "best_path": "Python → ML basics → LLM APIs → RAG → portfolio → internships.",
        "skills": ["Python", "Git/GitHub", "ML basics", "Prompt engineering", "RAG"],
        "tools": ["Python", "Streamlit", "LangChain", "FAISS/Chroma", "OpenAI/Gemini API"],
        "projects": ["AI Resume Reviewer", "PDF RAG Chatbot", "AI Job Search Assistant"],
        "roles": ["AI Intern", "GenAI Intern", "Junior AI Engineer"],
        "roadmap": {
            "30 Days": "Python, Git, ML basics, one mini ML project.",
            "60 Days": "Prompt engineering, LLM APIs, first Streamlit LLM app.",
            "90 Days": "RAG chatbot, deployment, GitHub portfolio, start applying.",
        },
    },
    "IT Professional": {
        "starting_from": "Strong coding/engineering base; new to AI.",
        "best_path": "Leverage backend skills → LLM APIs → RAG → agents → AI systems.",
        "skills": ["LLM APIs", "RAG", "Vector DBs", "AI agents", "Evaluation"],
        "tools": ["FastAPI", "LangChain", "LangGraph", "pgvector/Pinecone", "Docker"],
        "projects": ["Document Intelligence System", "AI Customer Support Assistant", "Multi-Agent Workflow"],
        "roles": ["AI Engineer", "GenAI Engineer", "Applied AI Engineer"],
        "roadmap": {
            "30 Days": "LLM APIs, prompt patterns, embeddings, one RAG proof-of-concept.",
            "60 Days": "Production RAG with FastAPI, evaluation, and monitoring.",
            "90 Days": "Agentic workflow + deployment; publish and interview.",
        },
    },
    "Non-IT Professional": {
        "starting_from": "Domain expertise; limited coding.",
        "best_path": "AI tools + prompts → light Python → no/low-code AI automation.",
        "skills": ["Prompt engineering", "AI tools", "Basic Python", "Automation", "Data literacy"],
        "tools": ["ChatGPT/Claude", "Streamlit", "Zapier/Make", "Google Sheets", "OpenAI API"],
        "projects": ["AI Newsletter Generator", "AI Analytics Dashboard", "AI Resume Analyzer"],
        "roles": ["AI Automation Specialist", "Prompt Engineer", "AI Product Associate"],
        "roadmap": {
            "30 Days": "Prompt engineering mastery + one automation using AI tools.",
            "60 Days": "Basic Python + a Streamlit app calling an LLM API.",
            "90 Days": "Domain-specific AI assistant + portfolio and case study.",
        },
    },
    "Data Analyst": {
        "starting_from": "SQL, Excel, dashboards, some Python.",
        "best_path": "Add LLMs + RAG on top of analytics for AI-driven insights.",
        "skills": ["Python", "LLM APIs", "RAG", "Embeddings", "Data storytelling"],
        "tools": ["Pandas", "LangChain", "Chroma", "Streamlit", "Plotly"],
        "projects": ["AI Analytics Dashboard", "Document Intelligence System", "AI Report Generator"],
        "roles": ["Applied AI Engineer", "AI Analyst", "GenAI Developer"],
        "roadmap": {
            "30 Days": "LLM APIs + embeddings applied to your existing datasets.",
            "60 Days": "RAG over reports/docs with a Streamlit front end.",
            "90 Days": "End-to-end AI analytics assistant + deployment.",
        },
    },
    "Software Engineer": {
        "starting_from": "Solid programming and system design.",
        "best_path": "LLM APIs → RAG → agents → AI platform/infra roles.",
        "skills": ["LLM APIs", "RAG", "AI agents", "System design", "Evaluation"],
        "tools": ["FastAPI", "LangGraph", "pgvector", "Docker", "LangSmith"],
        "projects": ["Multi-Agent Workflow", "AI Coding Assistant", "AI Customer Support Assistant"],
        "roles": ["AI Engineer", "Forward Deployed AI Engineer", "AI Solutions Architect"],
        "roadmap": {
            "30 Days": "LLM API integration patterns + a RAG service.",
            "60 Days": "Agentic system with tools, memory, and evaluation.",
            "90 Days": "Deployed, monitored AI system; system-design interviews.",
        },
    },
    "QA Engineer": {
        "starting_from": "Testing, automation, quality mindset.",
        "best_path": "Move into AI evaluation, testing, and observability roles.",
        "skills": ["LLM evaluation", "Prompt testing", "Python", "RAG basics", "Observability"],
        "tools": ["Python", "LangSmith", "Pytest", "Streamlit", "OpenAI API"],
        "projects": ["LLM Evaluation Harness", "AI Interview Coach", "RAG Quality Dashboard"],
        "roles": ["AI Evaluation Engineer", "AI QA Engineer", "Applied AI Engineer"],
        "roadmap": {
            "30 Days": "LLM basics + how to test prompts and outputs.",
            "60 Days": "Build an evaluation harness for a RAG app.",
            "90 Days": "Groundedness/latency/cost dashboards + interview prep.",
        },
    },
    "Product Manager": {
        "starting_from": "Product sense, user research, roadmapping.",
        "best_path": "Add AI literacy → become an AI Product Manager.",
        "skills": ["AI literacy", "Prompt design", "Evaluation", "AI UX", "Cost/latency tradeoffs"],
        "tools": ["ChatGPT/Claude", "Streamlit", "Notion", "Analytics tools", "OpenAI API"],
        "projects": ["AI Product Spec + Prototype", "AI Feature Evaluation", "AI Analytics Dashboard"],
        "roles": ["AI Product Manager", "AI Program Manager", "AI Product Owner"],
        "roadmap": {
            "30 Days": "How LLMs, RAG, and agents work at a conceptual level.",
            "60 Days": "Write an AI PRD; prototype with a no-code AI tool.",
            "90 Days": "Ship a small AI feature demo; learn evaluation metrics.",
        },
    },
    "Business Analyst": {
        "starting_from": "Requirements, stakeholder communication, data.",
        "best_path": "AI-enabled analysis + automation and assistant building.",
        "skills": ["Prompt engineering", "Basic Python", "RAG basics", "Automation", "Data literacy"],
        "tools": ["ChatGPT/Claude", "Streamlit", "Pandas", "Zapier/Make", "OpenAI API"],
        "projects": ["AI Requirements Assistant", "AI Report Generator", "AI Customer Support Assistant"],
        "roles": ["AI Business Analyst", "AI Automation Specialist", "AI Product Associate"],
        "roadmap": {
            "30 Days": "Prompt engineering + AI-assisted analysis workflows.",
            "60 Days": "Basic Python + a simple LLM-powered assistant.",
            "90 Days": "Domain assistant + a documented business case.",
        },
    },
}

# ---------------------------------------------------------------------------
# GenAI Role Explorer — role cards
# ---------------------------------------------------------------------------

GENAI_ROLES = {
    "AI Engineer": {
        "does": "Builds AI-powered features and services end to end.",
        "skills": ["Python", "LLM APIs", "RAG", "APIs/backends", "Deployment"],
        "tools": ["FastAPI", "LangChain", "Vector DBs", "Docker", "Cloud"],
        "projects": ["RAG Chatbot", "AI Customer Support Assistant"],
        "interview": ["LLM basics", "RAG design", "System design", "Python coding"],
        "keywords": ["LLM", "RAG", "FastAPI", "Vector DB", "Prompt engineering"],
        "prep": "Beginner: Python + LLM APIs. Advanced: production RAG + agents + deployment.",
        "best_for": "Developers who want to ship AI product features.",
    },
    "Generative AI Engineer": {
        "does": "Specializes in LLM apps, prompting, RAG, and generation quality.",
        "skills": ["Prompt engineering", "RAG", "Embeddings", "Evaluation", "LLM APIs"],
        "tools": ["LangChain", "LlamaIndex", "Chroma/Pinecone", "OpenAI/Anthropic API"],
        "projects": ["Document Intelligence System", "AI Newsletter Generator"],
        "interview": ["Prompt patterns", "RAG pipeline", "Hallucination control", "Evaluation"],
        "keywords": ["Generative AI", "LLM", "RAG", "Embeddings", "Evaluation"],
        "prep": "Beginner: prompting + embeddings. Advanced: eval, guardrails, cost control.",
        "best_for": "People who love LLM apps and generation quality.",
    },
    "LLM Engineer": {
        "does": "Works deep on LLM behavior, fine-tuning, and optimization.",
        "skills": ["Transformers", "Fine-tuning", "Embeddings", "Evaluation", "Python"],
        "tools": ["Hugging Face", "PyTorch", "LoRA/PEFT", "Weights & Biases"],
        "projects": ["Fine-tuned domain model", "LLM Evaluation Harness"],
        "interview": ["Transformer internals", "Fine-tuning vs RAG", "Tokenization", "Evaluation"],
        "keywords": ["LLM", "Fine-tuning", "Transformers", "Hugging Face", "Evaluation"],
        "prep": "Beginner: transformers + tokenization. Advanced: fine-tuning + serving.",
        "best_for": "Engineers who enjoy model internals and optimization.",
    },
    "RAG Engineer": {
        "does": "Builds retrieval pipelines that ground LLMs in real data.",
        "skills": ["Chunking", "Embeddings", "Vector search", "Retrieval tuning", "Evaluation"],
        "tools": ["LangChain", "LlamaIndex", "pgvector/Pinecone/FAISS", "Elasticsearch"],
        "projects": ["PDF RAG Chatbot", "Document Intelligence System"],
        "interview": ["Chunking strategy", "Hybrid search", "Reranking", "Groundedness"],
        "keywords": ["RAG", "Vector DB", "Embeddings", "Retrieval", "Reranking"],
        "prep": "Beginner: basic RAG. Advanced: hybrid search, reranking, evaluation.",
        "best_for": "People who like search, data, and grounding LLMs.",
    },
    "Prompt Engineer": {
        "does": "Designs, tests, and optimizes prompts and guardrails.",
        "skills": ["Prompt patterns", "Few-shot", "Structured output", "Evaluation", "Domain knowledge"],
        "tools": ["ChatGPT/Claude", "LangChain", "Prompt testing tools"],
        "projects": ["Prompt Library", "AI Interview Coach"],
        "interview": ["Few-shot vs zero-shot", "CoT", "JSON output", "Guardrails"],
        "keywords": ["Prompt engineering", "Few-shot", "Guardrails", "Structured output"],
        "prep": "Beginner: prompt patterns. Advanced: systematic prompt evaluation.",
        "best_for": "Detail-oriented people who like language and iteration.",
    },
    "AI Agent Engineer": {
        "does": "Builds autonomous, tool-using, multi-step AI systems.",
        "skills": ["Tool calling", "Agent workflows", "Memory", "Orchestration", "Evaluation"],
        "tools": ["LangGraph", "LangChain", "Function calling", "Vector DBs"],
        "projects": ["Multi-Agent Workflow System", "AI Job Search Agent"],
        "interview": ["Agent loops", "Tool use", "Memory design", "Failure handling"],
        "keywords": ["AI agents", "LangGraph", "Tool calling", "Orchestration"],
        "prep": "Beginner: single-tool agents. Advanced: multi-agent orchestration.",
        "best_for": "Systems thinkers who like automation and orchestration.",
    },
    "AI Automation Engineer": {
        "does": "Automates business workflows with AI + integrations.",
        "skills": ["Automation", "APIs", "Prompt engineering", "Python", "Integrations"],
        "tools": ["Zapier/Make", "Python", "LLM APIs", "Webhooks"],
        "projects": ["AI Newsletter Generator", "AI Customer Support Assistant"],
        "interview": ["Workflow design", "API integration", "Error handling", "Cost control"],
        "keywords": ["AI automation", "Workflows", "Integrations", "APIs"],
        "prep": "Beginner: no-code automations. Advanced: coded pipelines + monitoring.",
        "best_for": "Practical builders who like removing repetitive work.",
    },
    "AI Product Manager": {
        "does": "Defines and ships AI products; balances value, cost, and risk.",
        "skills": ["AI literacy", "Roadmapping", "Evaluation", "AI UX", "Stakeholder mgmt"],
        "tools": ["ChatGPT/Claude", "Analytics", "Notion", "Streamlit demos"],
        "projects": ["AI Product Spec + Prototype", "AI Feature Evaluation"],
        "interview": ["AI use-case sizing", "Metrics", "Risk/guardrails", "Prioritization"],
        "keywords": ["AI product", "Evaluation", "Roadmap", "AI UX"],
        "prep": "Beginner: AI concepts. Advanced: eval metrics + AI product strategy.",
        "best_for": "Product-minded people who can bridge tech and business.",
    },
    "Forward Deployed AI Engineer": {
        "does": "Works directly with customers to build and ship AI solutions.",
        "skills": ["Full-stack", "LLM APIs", "RAG", "Communication", "Rapid prototyping"],
        "tools": ["Python", "FastAPI", "React/Next.js", "Vector DBs", "Cloud"],
        "projects": ["Custom RAG for a client", "Multi-Agent Workflow System"],
        "interview": ["System design", "Customer scenarios", "Coding", "Tradeoffs"],
        "keywords": ["Forward deployed", "LLM", "RAG", "Full-stack", "Customer"],
        "prep": "Beginner: full-stack + LLM APIs. Advanced: customer-facing AI systems.",
        "best_for": "Engineers who enjoy customers and end-to-end delivery.",
    },
    "AI Solutions Architect": {
        "does": "Designs scalable, secure, cost-aware AI architectures.",
        "skills": ["System design", "RAG/agents", "Cloud", "Security", "Cost optimization"],
        "tools": ["Cloud (AWS/GCP/Azure)", "Vector DBs", "Docker/K8s", "Observability"],
        "projects": ["Enterprise RAG Architecture", "AI Platform Design"],
        "interview": ["Architecture", "Scaling", "Security", "Cost/latency tradeoffs"],
        "keywords": ["AI architecture", "Scalability", "Security", "Cloud"],
        "prep": "Beginner: cloud + RAG. Advanced: enterprise-grade AI architecture.",
        "best_for": "Senior engineers who like design and tradeoffs.",
    },
}

# ---------------------------------------------------------------------------
# Skill Roadmap — skill tree with metadata
# ---------------------------------------------------------------------------

SKILL_TREE = [
    ("Python Programming", "Core language for all AI work.", "Foundation for every AI task.",
     ["Python", "Jupyter", "VS Code"], "Build a CLI data tool.", "Beginner"),
    ("Machine Learning Basics", "Learn how models learn from data.", "Context for modern AI.",
     ["Scikit-learn", "Pandas"], "Churn prediction model.", "Beginner"),
    ("Deep Learning Basics", "Neural networks and training.", "Foundation for LLMs.",
     ["PyTorch", "Keras"], "Image classifier.", "Intermediate"),
    ("NLP", "Working with human language.", "Base for language models.",
     ["spaCy", "NLTK", "Hugging Face"], "Text classifier.", "Intermediate"),
    ("Transformers", "The architecture behind LLMs.", "Understand how LLMs work.",
     ["Hugging Face", "PyTorch"], "Use a pretrained transformer.", "Intermediate"),
    ("Large Language Models", "Using and prompting LLMs.", "Core of Generative AI.",
     ["OpenAI/Anthropic/Gemini API"], "Chatbot with an LLM API.", "Beginner"),
    ("Prompt Engineering", "Design effective prompts.", "Cheapest way to control LLMs.",
     ["ChatGPT/Claude", "LangChain"], "Prompt library with tests.", "Beginner"),
    ("Embeddings", "Turning text into vectors.", "Foundation for search & RAG.",
     ["OpenAI embeddings", "Sentence-Transformers"], "Semantic search demo.", "Intermediate"),
    ("Vector Databases", "Store and search embeddings.", "Backbone of RAG.",
     ["FAISS", "Chroma", "Pinecone", "pgvector"], "Vector search over docs.", "Intermediate"),
    ("RAG", "Ground LLMs in your data.", "Most in-demand GenAI skill.",
     ["LangChain", "LlamaIndex"], "PDF RAG chatbot.", "Intermediate"),
    ("LangChain", "Framework to build LLM apps.", "Speeds up app building.",
     ["LangChain"], "RAG pipeline with LangChain.", "Intermediate"),
    ("LangGraph", "Build stateful agent workflows.", "Powers reliable agents.",
     ["LangGraph"], "Two-step agent workflow.", "Advanced"),
    ("AI Agents", "Autonomous, tool-using systems.", "Fast-growing area.",
     ["LangGraph", "Function calling"], "Research agent.", "Advanced"),
    ("FastAPI", "Serve AI as APIs.", "Turn models into services.",
     ["FastAPI", "Uvicorn"], "Wrap a RAG app in an API.", "Intermediate"),
    ("Streamlit", "Build quick AI UIs.", "Great for demos & portfolios.",
     ["Streamlit"], "This dashboard!", "Beginner"),
    ("Cloud Deployment", "Ship apps to the web.", "Make projects live.",
     ["Render", "Railway", "HF Spaces", "AWS/GCP/Azure"], "Deploy a Streamlit app.", "Intermediate"),
    ("Docker", "Containerize your apps.", "Consistent deployments.",
     ["Docker"], "Dockerize a FastAPI app.", "Intermediate"),
    ("Evaluation and Monitoring", "Measure quality, cost, latency.", "Required for production.",
     ["LangSmith", "MLflow"], "Eval harness for a RAG app.", "Advanced"),
    ("Responsible AI", "Safety, bias, privacy, guardrails.", "Trust and compliance.",
     ["Guardrails", "Policies"], "Add guardrails to a chatbot.", "Intermediate"),
]

# ---------------------------------------------------------------------------
# Learning Roadmap — 30/60/90-day weekly plans
# ---------------------------------------------------------------------------

WEEKLY_ROADMAP = {
    "30 Days": [
        (1, "Python basics", "Variables, loops, functions, files", "Small Python script", "Comfortable with Python syntax"),
        (2, "Pandas, NumPy, Git", "Data handling + version control", "Data cleaning notebook", "Handle data + push to GitHub"),
        (3, "ML basics", "Regression, classification, evaluation", "Churn prediction model", "Train and evaluate a model"),
        (4, "LLM intro + prompt engineering", "Tokens, context, prompting", "Prompt library", "Write effective prompts"),
    ],
    "60 Days": [
        (5, "LLM APIs", "Calling OpenAI/Gemini from Python", "API-powered script", "Integrate an LLM API"),
        (6, "Streamlit", "Build interactive UIs", "LLM chat app", "Ship a working app"),
        (7, "Embeddings", "Vectors + semantic search", "Semantic search demo", "Understand embeddings"),
        (8, "Vector databases", "FAISS/Chroma basics", "Vector search over docs", "Store & query vectors"),
    ],
    "90 Days": [
        (9, "RAG", "Chunking, retrieval, grounding", "PDF RAG chatbot", "Build a full RAG app"),
        (10, "Deployment", "Docker + cloud hosting", "Deploy the RAG app", "App is live online"),
        (11, "AI agents", "Tool calling + workflows", "Simple agent", "Build a basic agent"),
        (12, "Resume, LinkedIn, applications", "Portfolio + job search", "3 polished projects", "Start applying"),
    ],
}

# ---------------------------------------------------------------------------
# Project Portfolio Builder
# ---------------------------------------------------------------------------

PROJECTS = [
    {
        "name": "PDF RAG Chatbot",
        "difficulty": "Intermediate",
        "resume_value": "Very High",
        "problem": "Users need answers from long PDFs without reading everything.",
        "persona": "Students, researchers, support teams.",
        "features": ["PDF upload", "Chunking", "Vector search", "Grounded answers", "Source citations"],
        "architecture": "Upload → extract text → chunk → embed → vector DB → retrieve → LLM → answer.",
        "tech": ["Python", "LangChain", "FAISS/Chroma", "Streamlit", "LLM API"],
        "vector_db": "FAISS or Chroma",
        "eval": ["Groundedness", "Answer relevance", "Latency", "Cost per query"],
        "deploy": "Streamlit Community Cloud or Render.",
        "bullets": [
            "Built a PDF-based RAG chatbot using Python, LangChain, FAISS, and Streamlit with source-cited answers.",
        ],
        "readme": ["Problem", "Features", "Architecture", "Tech stack", "Setup", "Screenshots", "Limitations"],
    },
    {
        "name": "AI Resume Analyzer",
        "difficulty": "Beginner",
        "resume_value": "High",
        "problem": "Candidates struggle to tailor resumes to job descriptions.",
        "persona": "Job seekers, freshers.",
        "features": ["Resume upload", "JD comparison", "Gap analysis", "Improvement suggestions"],
        "architecture": "Upload resume + JD → extract text → LLM compares → suggestions → UI.",
        "tech": ["Python", "Streamlit", "LLM API", "PDF parser"],
        "vector_db": "Not required",
        "eval": ["Suggestion usefulness", "Match score accuracy"],
        "deploy": "Streamlit Community Cloud.",
        "bullets": [
            "Developed an AI resume analyzer comparing resumes to job descriptions using LLM APIs and Streamlit.",
        ],
        "readme": ["Problem", "Features", "Tech stack", "Setup", "Screenshots", "Future work"],
    },
    {
        "name": "AI Job Search Agent",
        "difficulty": "Advanced",
        "resume_value": "Excellent",
        "problem": "Job seekers need personalized role, keyword, and prep guidance.",
        "persona": "Freshers and career switchers.",
        "features": ["Skill gap analysis", "Role suggestions", "Keyword generation", "Interview questions"],
        "architecture": "Input skills → agent plans → tools (search, generate) → personalized plan.",
        "tech": ["Python", "LangGraph", "LLM API", "Streamlit"],
        "vector_db": "Optional (for job/skill knowledge base)",
        "eval": ["Plan relevance", "Tool success rate", "Latency"],
        "deploy": "Render or Railway.",
        "bullets": [
            "Created an AI job search agent that analyzes skills and generates roles, keywords, and interview prep using LangGraph.",
        ],
        "readme": ["Problem", "Agent design", "Tools", "Tech stack", "Setup", "Limitations"],
    },
    {
        "name": "AI Customer Support Assistant",
        "difficulty": "Intermediate",
        "resume_value": "Very High",
        "problem": "Companies get many repetitive support questions.",
        "persona": "Support teams, SaaS companies.",
        "features": ["FAQ ingestion", "Semantic search", "AI answers", "Low-confidence escalation", "Analytics"],
        "architecture": "Ingest FAQs → embed → vector DB → retrieve → LLM answer → escalate if unsure.",
        "tech": ["Python", "FastAPI", "LangChain", "Vector DB", "Streamlit"],
        "vector_db": "Chroma or pgvector",
        "eval": ["Deflection rate", "Groundedness", "Escalation accuracy"],
        "deploy": "Docker + cloud.",
        "bullets": [
            "Built an AI support assistant using RAG and semantic search to auto-answer FAQs and escalate low-confidence queries.",
        ],
        "readme": ["Problem", "Features", "Architecture", "Tech stack", "API docs", "Setup"],
    },
    {
        "name": "AI Interview Coach",
        "difficulty": "Intermediate",
        "resume_value": "High",
        "problem": "Candidates need realistic practice and feedback.",
        "persona": "Job seekers, students.",
        "features": ["Role-based questions", "Answer feedback", "Scoring", "Follow-up questions"],
        "architecture": "Pick role → LLM asks → user answers → LLM scores + feedback.",
        "tech": ["Python", "Streamlit", "LLM API"],
        "vector_db": "Optional",
        "eval": ["Feedback quality", "Scoring consistency"],
        "deploy": "Streamlit Community Cloud.",
        "bullets": [
            "Built an AI interview coach that generates role-specific questions and scores answers with actionable feedback.",
        ],
        "readme": ["Problem", "Features", "Tech stack", "Setup", "Screenshots"],
    },
    {
        "name": "AI Newsletter Generator",
        "difficulty": "Beginner",
        "resume_value": "Medium",
        "problem": "Creators spend hours writing newsletters.",
        "persona": "Creators, marketers.",
        "features": ["Topic input", "Draft generation", "Tone control", "Editable output"],
        "architecture": "Topic → prompt template → LLM → draft → edit → export.",
        "tech": ["Python", "Streamlit", "LLM API"],
        "vector_db": "Not required",
        "eval": ["Draft quality", "Edit effort saved"],
        "deploy": "Streamlit Community Cloud.",
        "bullets": [
            "Developed an AI newsletter generator with tone control and editable drafts using LLM APIs and Streamlit.",
        ],
        "readme": ["Problem", "Features", "Tech stack", "Setup"],
    },
    {
        "name": "Document Intelligence System",
        "difficulty": "Advanced",
        "resume_value": "Excellent",
        "problem": "Enterprises need to extract structure and answers from documents.",
        "persona": "Enterprise, legal, finance teams.",
        "features": ["Multi-format ingest", "Extraction", "RAG Q&A", "Tables/entities", "Dashboards"],
        "architecture": "Ingest → parse → chunk → embed → vector DB → retrieve + extract → LLM → UI.",
        "tech": ["Python", "FastAPI", "LlamaIndex", "pgvector", "Streamlit/React"],
        "vector_db": "pgvector or Pinecone",
        "eval": ["Extraction accuracy", "Groundedness", "Latency", "Cost"],
        "deploy": "Docker + cloud + CI/CD.",
        "bullets": [
            "Built a document intelligence system with RAG Q&A and structured extraction using LlamaIndex and pgvector.",
        ],
        "readme": ["Problem", "Architecture", "Tech stack", "API docs", "Evaluation", "Setup"],
    },
    {
        "name": "AI Analytics Dashboard",
        "difficulty": "Intermediate",
        "resume_value": "High",
        "problem": "Non-technical users want to ask questions of their data.",
        "persona": "Analysts, business teams.",
        "features": ["Natural-language queries", "Charts", "Summaries", "Export"],
        "architecture": "Question → LLM → query/plan → compute → chart + summary.",
        "tech": ["Python", "Streamlit", "Pandas", "Plotly", "LLM API"],
        "vector_db": "Optional",
        "eval": ["Answer correctness", "Chart relevance"],
        "deploy": "Streamlit Community Cloud.",
        "bullets": [
            "Created an AI analytics dashboard letting users query data in natural language with auto-generated charts.",
        ],
        "readme": ["Problem", "Features", "Tech stack", "Setup", "Screenshots"],
    },
    {
        "name": "Multi-Agent Workflow System",
        "difficulty": "Advanced",
        "resume_value": "Excellent",
        "problem": "Complex tasks need multiple cooperating AI agents.",
        "persona": "Advanced builders, startups.",
        "features": ["Planner agent", "Worker agents", "Tool use", "Memory", "Human-in-the-loop"],
        "architecture": "Planner → delegates to workers → tools → aggregate → review → output.",
        "tech": ["Python", "LangGraph", "LLM API", "Vector DB", "FastAPI"],
        "vector_db": "Chroma or pgvector",
        "eval": ["Task success rate", "Tool reliability", "Cost", "Latency"],
        "deploy": "Docker + cloud.",
        "bullets": [
            "Built a multi-agent workflow system with a planner and worker agents using LangGraph, tools, and memory.",
        ],
        "readme": ["Problem", "Agent design", "Architecture", "Tech stack", "Evaluation", "Setup"],
    },
]

# ---------------------------------------------------------------------------
# RAG learning content
# ---------------------------------------------------------------------------

RAG_FLOW = [
    "User asks a question",
    "Question is converted into an embedding",
    "Vector database is searched for similar chunks",
    "Most relevant document chunks are retrieved",
    "Chunks + question are sent to the LLM as context",
    "LLM generates a grounded answer with sources",
]

RAG_COMPONENTS = [
    ("Document Loader", "Loads PDFs, docs, or web pages."),
    ("Text Splitter", "Breaks content into chunks."),
    ("Embedding Model", "Converts text into vectors."),
    ("Vector Database", "Stores and searches embeddings."),
    ("Retriever", "Finds the most relevant chunks."),
    ("LLM", "Generates the final answer."),
    ("Evaluation", "Checks accuracy, groundedness, and hallucination."),
]

RAG_CONCEPTS = {
    "Chunking": "Split documents into overlapping pieces so retrieval is precise. Too big = noisy, too small = lost context.",
    "Embeddings": "Numeric vectors that capture meaning so similar text is close together.",
    "Vector databases": "Specialized stores that find nearest vectors fast (FAISS, Chroma, Pinecone, pgvector).",
    "Retrieval": "Fetch the top-k most relevant chunks for a question, optionally with reranking.",
    "Hallucination reduction": "Ground answers in retrieved context, cite sources, and refuse when context is missing.",
}

# ---------------------------------------------------------------------------
# AI Tools section
# ---------------------------------------------------------------------------

AI_TOOLS = [
    ("Python", "Language", "The core language for all AI development."),
    ("Streamlit", "UI", "Quickly build interactive AI dashboards and demos."),
    ("FastAPI", "Backend", "Serve AI models and RAG apps as APIs."),
    ("LangChain", "Framework", "Compose LLM apps: chains, RAG, tools, agents."),
    ("LlamaIndex", "Framework", "Data framework focused on RAG and indexing."),
    ("OpenAI API", "LLM API", "Access GPT models for generation and embeddings."),
    ("Gemini API", "LLM API", "Google's multimodal LLM API."),
    ("Hugging Face", "Models", "Open models, datasets, and Spaces hosting."),
    ("FAISS", "Vector DB", "Fast local similarity search library."),
    ("Chroma", "Vector DB", "Simple developer-friendly vector database."),
    ("Pinecone", "Vector DB", "Managed, scalable vector database service."),
    ("Docker", "DevOps", "Containerize apps for consistent deployment."),
    ("GitHub", "DevOps", "Version control and portfolio hosting."),
    ("Cloud (AWS/GCP/Azure)", "Cloud", "Host, scale, and secure AI applications."),
]

# ---------------------------------------------------------------------------
# Interview preparation
# ---------------------------------------------------------------------------

# Senior / high-signal interview prep. Each item is (question, answer, key_points).
# The answers assume modern GenAI engineering (2025-2026): agentic systems,
# retrieval infra, LLMOps, evaluation, and production cost/latency tradeoffs.
INTERVIEW_QA = {
    "LLM Systems Design": [
        ("Design a production RAG assistant over 10M enterprise documents.",
         "Split it into an offline indexing plane and an online serving plane. Offline: "
         "ingest connectors, layout-aware parsing, semantic + structural chunking, "
         "embedding generation, and an ANN index (HNSW/IVF-PQ) plus a keyword index for "
         "hybrid search, with incremental re-indexing on document change. Online: query "
         "rewriting, hybrid retrieval, a cross-encoder reranker, context assembly under a "
         "token budget, the LLM call with structured output and citations, and guardrails. "
         "Wrap it with semantic caching, streaming responses, per-tenant isolation, an "
         "eval harness, and observability for cost, latency, and groundedness.",
         ["Offline vs online planes", "Hybrid retrieval + rerank", "Token-budgeted context",
          "Caching + streaming", "Multi-tenant isolation", "Eval + observability"]),
        ("How do you take latency (p95) from 8s to under 2s without hurting quality?",
         "Profile the pipeline first — usually retrieval + reranking + generation dominate. "
         "Levers: semantic caching of frequent queries, streaming tokens so time-to-first-token "
         "is low, a smaller/faster model or distilled model for easy queries with a router to a "
         "stronger model for hard ones, parallelizing retrieval and reranking, cutting context "
         "size with better retrieval, prompt caching / KV-cache reuse, and speculative decoding. "
         "Validate each change against an eval set so quality does not regress.",
         ["Profile before optimizing", "Streaming / TTFT", "Model routing + distillation",
          "Prompt/KV caching", "Speculative decoding", "Guard quality with evals"]),
        ("How would you design a multi-tenant LLM platform for many internal teams?",
         "Central gateway in front of all providers for auth, rate limiting, budget quotas, "
         "routing, retries, and fallbacks. Per-tenant data isolation in the vector store "
         "(namespace or row-level security), a shared prompt/version registry, a unified eval "
         "and observability layer, PII redaction and guardrails as middleware, and cost "
         "attribution per team. Abstract providers so you can swap models without app changes.",
         ["LLM gateway", "Provider abstraction + fallback", "Tenant isolation",
          "Budgets + cost attribution", "Central evals + guardrails"]),
    ],
    "RAG & Retrieval": [
        ("Naive RAG returns irrelevant chunks. Walk me through fixing retrieval quality.",
         "Treat retrieval as a search problem. Improve chunking (layout-aware, semantic, with "
         "overlap and metadata), use hybrid search (dense + BM25) to catch exact terms, add a "
         "cross-encoder reranker on the top candidates, and apply query transformation "
         "(rewriting, HyDE, multi-query) for vague questions. Add metadata filtering, tune "
         "top-k, and measure with retrieval metrics (recall@k, MRR, nDCG) plus end-to-end "
         "groundedness — not vibes.",
         ["Better chunking + metadata", "Hybrid dense+sparse", "Cross-encoder reranking",
          "Query rewriting / HyDE", "Measure recall@k, nDCG, groundedness"]),
        ("When is RAG the wrong tool, and what do you use instead?",
         "RAG fits knowledge that changes and must be cited. It is wrong when the task needs "
         "behavior/format/style (use fine-tuning), when the whole corpus fits in a long-context "
         "window and freshness is not an issue (long-context prompting), or when the task is "
         "reasoning/action over systems (agents + tools). In practice these combine: agentic "
         "RAG with fine-tuned components and long-context for large single documents.",
         ["RAG = fresh, citable knowledge", "Fine-tune = behavior/format",
          "Long-context vs RAG tradeoff", "Agents for actions", "Hybrid in practice"]),
        ("What is agentic / GraphRAG and when is it worth the extra cost?",
         "Agentic RAG lets the model plan multi-step retrieval — decompose the question, "
         "retrieve iteratively, and self-critique before answering. GraphRAG builds a knowledge "
         "graph so retrieval can traverse relationships and answer global questions a flat "
         "vector search misses. Both add latency and cost, so reserve them for complex, "
         "multi-hop, or corpus-wide questions and keep single-hop queries on plain RAG.",
         ["Iterative, planned retrieval", "Knowledge-graph traversal", "Multi-hop questions",
          "Cost/latency tradeoff", "Route by query complexity"]),
    ],
    "AI Agents & Orchestration": [
        ("Design a reliable agent for a real workflow (not a demo).",
         "Constrain it. Define a clear tool schema with typed inputs/outputs, a bounded plan "
         "(graph over free-form loops), explicit state and memory, and a critic/verifier step. "
         "Add retries with backoff, guardrails on tool calls, human-in-the-loop for risky "
         "actions, and hard stop conditions (max steps, budget) to prevent runaway loops. "
         "Instrument every step for tracing and build an eval set of real tasks to measure "
         "task-success rate and tool-call accuracy.",
         ["Typed tool schemas", "Bounded graph over loops", "Critic/verifier + HITL",
          "Stop conditions + budgets", "Trace + eval task success"]),
        ("What is MCP (Model Context Protocol) and why does it matter?",
         "MCP is an open standard for connecting models to tools and data through a uniform "
         "interface, so you build a capability once and any MCP-compatible client can use it. "
         "It matters because it decouples agents from bespoke integrations — the same "
         "filesystem, database, or API server works across models and frameworks, which is the "
         "direction the ecosystem is standardizing on.",
         ["Open tool/data standard", "Build once, reuse anywhere", "Decouples agent + tools",
          "Interoperable across models"]),
        ("Single powerful agent vs multi-agent system — how do you choose?",
         "Default to the simplest thing that works. A single well-scoped agent with good tools "
         "is easier to debug and cheaper. Go multi-agent when the problem has genuinely "
         "separable roles (planner/researcher/writer/critic) or needs parallelism, but expect "
         "more coordination overhead, latency, and failure modes. Orchestrate with an explicit "
         "graph and clear handoffs, not emergent chatter.",
         ["Prefer simplest design", "Separable roles / parallelism", "Coordination overhead",
          "Explicit orchestration graph"]),
    ],
    "LLMOps & Evaluation": [
        ("How do you evaluate an LLM/RAG feature without human labels for everything?",
         "Layered evals. Component metrics (retrieval recall@k, nDCG), task metrics "
         "(answer correctness, groundedness/faithfulness, context relevance via frameworks like "
         "RAGAS), and LLM-as-judge for open-ended quality — calibrated against a small "
         "human-labeled golden set to trust the judge. Run these in CI on every prompt/model "
         "change, track regressions, and complement offline evals with online signals (thumbs, "
         "escalation rate, task completion).",
         ["Layered: component + task + judge", "RAGAS-style groundedness",
          "Calibrate judge vs golden set", "Evals in CI", "Online + offline signals"]),
        ("How do you catch and reduce hallucinations in production?",
         "Prevention + detection. Prevention: ground answers in retrieved context, constrain "
         "the prompt to that context, require citations, and refuse when evidence is missing. "
         "Detection: a groundedness/faithfulness check (NLI or LLM-judge) comparing the answer "
         "to sources, flagging or blocking unsupported claims. Monitor a hallucination rate "
         "metric and alert on drift after model or data changes.",
         ["Grounding + forced citations", "Refuse without evidence", "Faithfulness check",
          "Track hallucination rate", "Alert on drift"]),
        ("What does an LLM observability stack look like and why is it non-negotiable?",
         "Trace every request end to end — prompt, retrieved context, tool calls, tokens, "
         "latency, cost, and output — with tools like LangSmith or Langfuse. You need it to "
         "debug non-deterministic failures, attribute cost, catch regressions from silent "
         "model updates, and feed real traffic back into eval sets. Without it you are flying "
         "blind on a system whose behavior shifts under you.",
         ["End-to-end tracing", "Cost + token attribution", "Debug non-determinism",
          "Regression detection", "Traffic -> eval sets"]),
    ],
    "Prompt & Context Engineering": [
        ("What is 'context engineering' and how is it more than prompt engineering?",
         "Context engineering is designing everything that enters the context window — system "
         "instructions, retrieved evidence, tool outputs, memory, and few-shot examples — under "
         "a token budget for accuracy and cost. It goes beyond wording a prompt: it is deciding "
         "what to retrieve, how to compress/summarize, how to order information (recency and "
         "position effects), and what to leave out. In agentic systems it is the core "
         "reliability lever.",
         ["Whole context window design", "Token budgeting", "Retrieval + compression",
          "Ordering / position effects", "Core agent reliability lever"]),
        ("How do you get reliable structured output from an LLM at scale?",
         "Use native structured-output / JSON-schema or function-calling modes instead of "
         "parsing free text, validate against a schema (e.g. Pydantic), and on failure "
         "re-ask with the validation error. Keep the schema tight, provide one or two "
         "examples, and add guardrails for enums/ranges. This makes the model a dependable "
         "component other services can consume.",
         ["Native structured output / JSON schema", "Schema validation (Pydantic)",
          "Re-ask on validation error", "Tight schema + examples"]),
    ],
    "Retrieval & Vector Infra": [
        ("Compare vector index choices and when each fits.",
         "HNSW gives excellent recall/latency but is memory-hungry — great for moderate scale "
         "and low latency. IVF-PQ compresses vectors for huge corpora at some recall cost. "
         "pgvector keeps vectors next to relational data and transactions (simple ops, one "
         "system); managed services like Pinecone trade cost for scale and zero-ops. Choose on "
         "scale, latency target, filtering needs, and operational appetite — and always "
         "support metadata filtering and hybrid search.",
         ["HNSW vs IVF-PQ tradeoffs", "pgvector = colocated + transactional",
          "Managed vs self-hosted", "Filtering + hybrid support", "Pick by scale/latency/ops"]),
        ("How do you keep an embedding index correct as data and models change?",
         "Treat embeddings as versioned artifacts. On document change, incrementally re-embed "
         "and upsert with stable IDs and metadata (source, version, timestamp). Changing the "
         "embedding model requires a full re-index behind a new index version with a cutover, "
         "since vectors are not comparable across models. Automate freshness checks and monitor "
         "for stale or orphaned vectors.",
         ["Versioned embeddings", "Incremental upsert by ID", "Model change = full re-index",
          "Cutover between index versions", "Freshness monitoring"]),
    ],
    "Model Optimization & Fine-tuning": [
        ("RAG vs fine-tuning vs prompting — how do you decide, with tradeoffs?",
         "Prompting/few-shot: fastest, no training, best first attempt. RAG: inject fresh, "
         "citable knowledge without retraining — best for changing facts. Fine-tuning "
         "(usually LoRA/QLoRA): teach behavior, format, tone, or a narrow skill, and can "
         "shrink prompts and cost — but it is stale on new facts and needs data + eval "
         "discipline. Real systems combine them: a fine-tuned model for behavior + RAG for "
         "knowledge.",
         ["Prompt = fast baseline", "RAG = fresh knowledge", "Fine-tune = behavior/format",
          "LoRA/QLoRA efficiency", "Combine in practice"]),
        ("How do you serve a model cheaper without a big quality drop?",
         "Quantization (int8/int4) to cut memory and speed inference, distillation to a smaller "
         "student for routine traffic, batching and KV-cache reuse, prompt caching, and a "
         "router that sends easy queries to a cheap model and only escalates hard ones. "
         "Measure the quality/cost curve on an eval set and pick the knee, not the extreme.",
         ["Quantization int8/int4", "Distillation for routine traffic", "Batching + KV cache",
          "Cost-based routing", "Pick the quality/cost knee"]),
    ],
    "Behavioral (Impact & Ownership)": [
        ("Tell me about an AI system you shipped and the impact.",
         "Use STAR with metrics and tradeoffs, not a feature list. Situation: the problem and "
         "who felt it. Task: your measurable goal (e.g. cut support handle time). Action: the "
         "key design decisions and why you rejected alternatives. Result: quantified impact "
         "(latency, deflection, cost) plus what you would change next. Senior signal is "
         "owning tradeoffs and outcomes, not tools.",
         ["STAR with metrics", "Design decisions + rejected options", "Quantified impact",
          "Own tradeoffs, not tools"]),
        ("How do you make an AI feature safe and trustworthy before launch?",
         "Define acceptable behavior and failure modes up front, add input/output guardrails "
         "(PII, prompt-injection, toxicity), ground and cite answers, gate risky actions behind "
         "human review, run red-teaming and an eval suite as a launch gate, and ship behind a "
         "flag with monitoring and a rollback path. Treat responsible AI as an engineering "
         "requirement, not an afterthought.",
         ["Define behavior + failure modes", "Guardrails: PII/injection/toxicity",
          "Red-team + eval gate", "Flagged rollout + rollback"]),
    ],
}

# Reference architecture shown on the System Design topic, as two pipeline lanes.
INTERVIEW_SYSTEM_DESIGN = {
    "Offline indexing plane": [
        "Sources / connectors", "Layout-aware parsing", "Semantic chunking + metadata",
        "Embeddings", "ANN index + keyword index",
    ],
    "Online serving plane": [
        "User query", "Query rewrite", "Hybrid retrieval", "Cross-encoder rerank",
        "Token-budgeted context", "LLM + structured output", "Guardrails + citations",
        "Streamed answer",
    ],
    "Cross-cutting": [
        "Semantic cache", "Observability: cost / latency / groundedness",
    ],
}

# ---------------------------------------------------------------------------
# Resume & LinkedIn
# ---------------------------------------------------------------------------

RESUME_SUMMARY = (
    "Aspiring Generative AI Engineer with hands-on experience building LLM-powered "
    "applications using Python, Streamlit, LangChain, and vector databases. Skilled in "
    "prompt engineering, embeddings, RAG architecture, API integration, and deployment. "
    "Built projects including a PDF RAG chatbot, AI resume analyzer, and AI customer "
    "support assistant. Seeking an entry-level AI/GenAI role to build production-ready AI solutions."
)

RESUME_BULLETS = [
    "Built a PDF-based RAG chatbot using Python, LangChain, FAISS, and Streamlit with source-cited answers.",
    "Developed an AI resume analyzer comparing resumes to job descriptions using LLM APIs.",
    "Created an AI customer support assistant using semantic search and prompt engineering.",
    "Deployed GenAI apps to the cloud and documented them with clean GitHub READMEs.",
]

LINKEDIN_HEADLINES = [
    "Aspiring Generative AI Engineer | Python | LLMs | RAG | LangChain | Streamlit | Building AI Projects",
    "Junior AI Engineer | GenAI | RAG Applications | Python | FastAPI | Vector Databases",
    "GenAI Developer | LLM Apps | Prompt Engineering | AI Automation | Portfolio Builder",
]

LINKEDIN_ABOUT = (
    "I build practical Generative AI applications using Python, LLM APIs, LangChain, and "
    "vector databases. Recently I built a PDF RAG chatbot, an AI resume analyzer, and an AI "
    "support assistant, focusing on retrieval quality, grounded answers, and clean deployment. "
    "I'm looking for entry-level AI/GenAI opportunities where I can keep shipping and learning."
)

GITHUB_TIPS = [
    "Pin your 3 strongest GenAI projects.",
    "Each repo: clear README with problem, architecture, setup, screenshots, and demo link.",
    "Add architecture diagrams and a short demo video (Loom/YouTube).",
    "Write meaningful commit messages and keep secrets out of the repo.",
    "Add a profile README summarizing your skills and projects.",
]

PORTFOLIO_CHECKLIST = [
    "3+ GenAI projects on GitHub",
    "At least one deployed live app",
    "Clean READMEs with screenshots",
    "LinkedIn headline + About updated",
    "Resume with project-based bullets",
    "Demo video for your best project",
]

# ---------------------------------------------------------------------------
# Job search strategy
# ---------------------------------------------------------------------------

JOB_TITLES = [
    "AI Intern", "Generative AI Intern", "Machine Learning Intern", "LLM Intern",
    "RAG Developer Intern", "Prompt Engineer Intern", "AI Automation Intern",
    "Junior AI Engineer", "Applied AI Engineer", "AI Solutions Engineer",
    "Forward Deployed Engineer",
]

BOOLEAN_SEARCHES = [
    '("Generative AI Intern" OR "LLM Intern" OR "AI Intern") AND (Python OR LangChain OR RAG)',
    '("Junior AI Engineer" OR "Applied AI Engineer") AND (RAG OR "vector database" OR LLM)',
    '("Prompt Engineer" OR "AI Automation") AND (Python OR LangChain OR OpenAI)',
]

WEEKLY_JOB_PLAN = [
    ("Apply to jobs", "30-50 applications"),
    ("Send LinkedIn requests", "20 requests"),
    ("Message recruiters/founders", "10 messages"),
    ("Post a project update", "1 post"),
    ("Improve a GitHub project", "1 improvement"),
    ("Practice mock interviews", "2 mock interviews"),
]

RECRUITER_MESSAGE = (
    "Hi [Name], I'm actively looking for entry-level opportunities in Generative AI / AI "
    "Engineering. I've built hands-on projects using Python, LLM APIs, LangChain, RAG, and "
    "vector databases, including a PDF RAG chatbot and an AI resume analyzer. I'd be grateful "
    "if you'd consider me for any relevant internship or junior AI role — happy to share my "
    "resume and GitHub portfolio. Thank you!"
)

NETWORKING_TIPS = [
    "Post 1-2 project updates per week to build visibility.",
    "Comment thoughtfully on AI practitioners' posts.",
    "Join AI communities and Discords; share what you build.",
    "Reach out to alumni and engineers for short informational chats.",
]

# ---------------------------------------------------------------------------
# Future AI opportunities
# ---------------------------------------------------------------------------

FUTURE_TRENDS = [
    ("AI Agents", "Autonomous, tool-using systems that complete multi-step tasks.",
     ["AI agents", "LangGraph", "Tool calling", "Orchestration"]),
    ("Multimodal AI", "Models that handle text, images, audio, and video together.",
     ["Multimodal APIs", "Vision", "Speech", "Prompting"]),
    ("RAG Systems", "Grounding LLMs in private and enterprise data.",
     ["RAG", "Vector DBs", "Retrieval tuning", "Evaluation"]),
    ("AI Automation", "Automating business workflows end to end.",
     ["Automation", "Integrations", "APIs", "Prompt engineering"]),
    ("AI Product Engineering", "Shipping reliable AI features in products.",
     ["LLM APIs", "AI UX", "Evaluation", "Cost control"]),
    ("AI Governance", "Safety, compliance, and responsible AI.",
     ["Responsible AI", "Policy", "Guardrails", "Risk"]),
    ("Evaluation & Observability", "Measuring and monitoring AI quality in production.",
     ["Evaluation", "LangSmith/MLflow", "Monitoring", "Groundedness"]),
    ("Domain-Specific Assistants", "AI tailored to finance, healthcare, education, legal.",
     ["RAG", "Domain data", "Guardrails", "Fine-tuning"]),
]

# ---------------------------------------------------------------------------
# Progress tracker areas (defaults)
# ---------------------------------------------------------------------------

PROGRESS_AREAS = {
    "Python": 60,
    "GenAI": 40,
    "RAG": 30,
    "Projects": 50,
    "Interview Prep": 25,
    "Resume/LinkedIn": 35,
    "Job Applications": 20,
}

# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------

AUTHOR = "Abhinav Konduri"
LINKEDIN_URL = "linkedin.com/in/abhinav-kanduri-a943b9353"
