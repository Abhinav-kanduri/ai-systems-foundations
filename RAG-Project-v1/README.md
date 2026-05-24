# RAG Pipeline Project

This project is an end-to-end guide for setting up a Retrieval-Augmented Generation
(RAG) pipeline. A RAG pipeline combines a language model with a searchable
knowledge base so the model can answer questions using your own documents instead
of relying only on its training data.

## What This Pipeline Does

The pipeline follows this flow:

1. Load source documents.
2. Clean and split documents into smaller chunks.
3. Convert chunks into embeddings.
4. Store embeddings in a vector database.
5. Retrieve relevant chunks for a user question.
6. Send the question plus retrieved context to an LLM.
7. Return a grounded answer with optional source references.

```text
Documents
   |
   v
Load -> Clean -> Chunk -> Embed -> Store in Vector DB
                                      |
User Question                         |
   |                                  v
   +-------------> Retrieve Relevant Context
                                      |
                                      v
                          Prompt LLM with Context
                                      |
                                      v
                              Final Answer
```

## Recommended Project Structure

Use this structure as the project grows:

```text
RAG-Project-v1/
  README.md
  requirements.txt
  .env.example
  data/
    raw/
    processed/
  src/
    config.py
    load_documents.py
    chunk_documents.py
    build_index.py
    retrieve.py
    rag_pipeline.py
    app.py
  notebooks/
    rag_experiment.ipynb
  tests/
    test_chunking.py
    test_retrieval.py
```

## Prerequisites

Install the following before running the project:

- Python 3.10 or newer
- Git
- An API key for your LLM provider, such as OpenAI, Azure OpenAI, Anthropic, or
  a local model runtime
- A vector database, such as Chroma, FAISS, Pinecone, Weaviate, or Qdrant

For a local beginner-friendly setup, Chroma or FAISS is recommended.

## 1. Create and Activate a Virtual Environment

From the project folder:

```powershell
cd C:\Users\abhin\ai-systems-foundations\RAG-Project-v1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again.

## 2. Install Dependencies

Create a `requirements.txt` file with:

```text
python-dotenv
langchain
langchain-community
langchain-openai
langchain-chroma
langchain-text-splitters
chromadb
tiktoken
pypdf
streamlit
```

Install them:

```powershell
pip install -r requirements.txt
```

Optional alternatives:

- Use `faiss-cpu` instead of `chromadb` for a FAISS-based local vector store.
- Use `sentence-transformers` if you want local embedding models.
- Use `unstructured` if you need advanced document parsing.

## 3. Configure Environment Variables

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4.1-mini
VECTOR_DB_PATH=./data/vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

Also create `.env.example` so the required settings are clear without exposing
secrets:

```text
OPENAI_API_KEY=
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4.1-mini
VECTOR_DB_PATH=./data/vector_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

Do not commit your real `.env` file to Git.

## 4. Add Source Documents

Place documents in:

```text
data/raw/
```

Example supported files:

- `.pdf`
- `.txt`
- `.md`
- `.docx`, if you add a compatible loader
- `.csv`, if your RAG use case includes tabular data

Start with a small number of documents first so ingestion and retrieval are easy
to debug.

## 5. Load Documents

Document loading reads files from `data/raw/` and converts them into text records
with metadata such as file name, page number, or source path.

Example loader logic:

```python
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_documents(data_dir: str = "data/raw"):
    documents = []

    for path in Path(data_dir).rglob("*"):
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            documents.extend(loader.load())
        elif path.suffix.lower() in [".txt", ".md"]:
            loader = TextLoader(str(path), encoding="utf-8")
            documents.extend(loader.load())

    return documents
```

Good metadata is important because it allows answers to cite where information
came from.

## 6. Chunk Documents

Large documents should be split into chunks before embedding. Chunking improves
retrieval quality because the vector database can return the most relevant
sections instead of entire files.

Example chunking logic:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents, chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    return splitter.split_documents(documents)
```

Recommended starting values:

- `CHUNK_SIZE=800` to `1200`
- `CHUNK_OVERLAP=100` to `200`

Use larger chunks for conceptual documents and smaller chunks for dense technical
content.

## 7. Create Embeddings and Build the Vector Index

Embeddings convert each chunk into a numeric representation of its meaning. The
vector database stores those embeddings and performs similarity search.

Example Chroma index setup:

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def build_index(chunks, persist_directory="data/vector_db"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )

    return vector_store
```

The `langchain-chroma` package provides the Chroma integration used in this
example.

## 8. Retrieve Relevant Context

Retrieval searches the vector database for chunks most similar to the user query.

Example retriever:

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def get_retriever(persist_directory="data/vector_db", k=4):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )

    return vector_store.as_retriever(search_kwargs={"k": k})
```

Start with `k=3` or `k=4`. Increase it if answers miss important context.

## 9. Generate an Answer

The generation step sends the user question and retrieved context to the LLM.

Example RAG prompt:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


PROMPT = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant. Answer the question using only the context below.
    If the answer is not in the context, say you do not know.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def answer_question(question, retriever):
    docs = retriever.invoke(question)
    context = format_docs(docs)

    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    chain = PROMPT | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "question": question,
    })

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs],
    }
```

Keep `temperature=0` for factual question answering.

## 10. Run the Full Pipeline

Typical first run:

```powershell
python src/load_documents.py
python src/chunk_documents.py
python src/build_index.py
python src/rag_pipeline.py
```

Or combine ingestion into one script:

```powershell
python src/build_index.py
```

Then ask a question:

```powershell
python src/rag_pipeline.py "What are the key ideas in these documents?"
```

## 11. Optional Streamlit App

For a simple UI, create `src/app.py`:

```python
import streamlit as st

from rag_pipeline import answer_question
from retrieve import get_retriever


st.set_page_config(page_title="RAG Pipeline", layout="wide")
st.title("RAG Pipeline")

question = st.text_input("Ask a question")

if question:
    retriever = get_retriever()
    result = answer_question(question, retriever)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    st.json(result["sources"])
```

Run it:

```powershell
streamlit run src/app.py
```

## 12. Evaluate the Pipeline

Test the system with questions where you already know the answer.

Track:

- Retrieval accuracy: Are the returned chunks relevant?
- Answer faithfulness: Does the answer stay grounded in the documents?
- Source quality: Are citations useful?
- Missing-answer behavior: Does the model say it does not know when context is
  insufficient?
- Latency: Is the response fast enough?
- Cost: Are chunk size, retrieval count, and model choice reasonable?

Example evaluation questions:

```text
What is the main topic of the documents?
Which document explains retrieval?
What assumptions are stated in the source material?
What information is missing from the documents?
```

## 13. Common Problems and Fixes

### No Documents Are Loaded

Check that files are inside:

```text
data/raw/
```

Also confirm your loader supports the file extension.

### Poor Answers

Try:

- Smaller chunks
- More overlap
- Increasing retrieval `k`
- Better document cleaning
- Adding source metadata
- Rewriting the prompt to require grounded answers

### Hallucinated Answers

Use a stricter prompt:

```text
Answer only from the provided context. If the answer is not present, say:
"I do not know based on the provided documents."
```

Also use `temperature=0`.

### Slow Indexing

Try:

- Indexing fewer documents during development
- Using a smaller embedding model
- Caching processed chunks
- Running ingestion separately from question answering

### Vector Database Not Updating

Delete the local vector database and rebuild:

```powershell
Remove-Item -Recurse -Force .\data\vector_db
python src/build_index.py
```

## 14. Production Checklist

Before using the RAG pipeline in a production-style workflow:

- Add logging.
- Add tests for chunking and retrieval.
- Store document IDs and source metadata.
- Add duplicate document detection.
- Add access control if documents are private.
- Add evaluation datasets.
- Monitor cost, latency, and failure rates.
- Separate ingestion from serving.
- Version your index when documents change.

## 15. Suggested Development Milestones

1. Load one PDF and print extracted text.
2. Split the document into chunks.
3. Embed chunks and store them in Chroma.
4. Run similarity search for a question.
5. Pass retrieved chunks into an LLM prompt.
6. Return an answer and source metadata.
7. Add a Streamlit interface.
8. Add evaluation questions.
9. Improve chunking and retrieval based on failures.

## Minimal End-to-End Example

Once the project files are implemented, the expected usage should look like:

```powershell
cd C:\Users\abhin\ai-systems-foundations\RAG-Project-v1
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Add documents to data/raw first.
python src/build_index.py
python src/rag_pipeline.py "What does the document say about RAG?"
```

## Notes

RAG quality depends more on document preparation and retrieval quality than on
the final LLM call alone. If the retrieved context is weak, the final answer will
also be weak. Start small, inspect retrieved chunks often, and improve the data
pipeline before tuning the model.
