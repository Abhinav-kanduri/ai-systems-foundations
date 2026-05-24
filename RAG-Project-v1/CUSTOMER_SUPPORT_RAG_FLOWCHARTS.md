# Customer Support RAG Application Flowcharts

This document shows an end-to-end Retrieval-Augmented Generation (RAG) flow for a
customer support application used by both customers and customer service agents.

# Author - Abhinav Kanduri

- Linkedin : https://www.linkedin.com/in/abhinav-kanduri-a943b9353/
This project is only for learning purpose and understand the latest concepts such as LLM, RAG AI Agentic frameworks, PROMPT ENGINEERING WORKS, CONTEXT MANAGEMENT.

## Problem Statement

A company wants to build a customer support assistant that can answer questions
from product manuals, FAQs, troubleshooting guides, policy documents, support
tickets, and internal knowledge-base articles.

The application has two main users:

1. Customers, who ask questions and receive quick self-service answers.
2. Customer service agents, who use retrieved context and generated suggestions
   to resolve tickets faster.

The goal is to provide accurate, grounded, source-backed answers while reducing
manual lookup time for support teams.

## High-Level RAG System Flow

``` mermaid
flowchart TD
    A[Support Documents] --> B[Document Ingestion]
    B --> C[Text Extraction]
    C --> D[Cleaning and Normalization]
    D --> E[Chunking]
    E --> F[Embedding Model]
    F --> G[(Vector Database)]

    H[Customer or Agent Question] --> I[Query Processing]
    I --> J[Query Embedding]
    J --> K[Similarity Search]
    G --> K
    K --> L[Relevant Context Chunks]
    L --> M[Prompt Builder]
    H --> M
    M --> N[LLM]
    N --> O[Grounded Answer]
    O --> P[Sources and Citations]
    O --> Q[Application Response]
```

## Customer Self-Service Flow

```mermaid
flowchart TD
    A[Customer Opens Support App] --> B[Customer Enters Question]
    B --> C{Is Question Clear?}

    C -- No --> D[Ask Clarifying Question]
    D --> B

    C -- Yes --> E[Search Knowledge Base]
    E --> F{Relevant Context Found?}

    F -- Yes --> G[Generate Answer Using Retrieved Context]
    G --> H[Show Answer with Sources]
    H --> I{Did This Resolve the Issue?}

    I -- Yes --> J[Close Self-Service Session]
    I -- No --> K[Offer Escalation to Support Agent]

    F -- No --> K
    K --> L[Create Support Ticket]
    L --> M[Attach Conversation History and Retrieved Evidence]
    M --> N[Route Ticket to Customer Service Agent]
```

## Customer Service Agent Flow

```mermaid
flowchart TD
    A[Agent Opens Ticket Queue] --> B[Select Customer Ticket]
    B --> C[View Customer Question and Conversation History]
    C --> D[Run RAG Retrieval]
    D --> E[Retrieve Similar Tickets, Policies, FAQs, and Product Docs]
    E --> F[Generate Suggested Response]
    F --> G[Show Sources and Confidence Signals]

    G --> H{Agent Approves Suggestion?}
    H -- Yes --> I[Send Response to Customer]
    H -- Needs Edit --> J[Agent Edits Response]
    J --> I
    H -- No --> K[Agent Searches Manually or Escalates]

    I --> L{Issue Resolved?}
    L -- Yes --> M[Close Ticket]
    L -- No --> N[Continue Conversation]
    N --> D
```

## End-to-End Customer Support RAG Workflow

```mermaid
flowchart LR
    subgraph Data_Preparation[Data Preparation]
        A1[FAQs]
        A2[Product Manuals]
        A3[Policy Docs]
        A4[Historical Tickets]
        A5[Troubleshooting Guides]

        A1 --> B[Ingestion Pipeline]
        A2 --> B
        A3 --> B
        A4 --> B
        A5 --> B

        B --> C[Clean Text]
        C --> D[Split into Chunks]
        D --> E[Create Embeddings]
        E --> F[(Vector Store)]
    end

    subgraph Runtime[Runtime Support Experience]
        G[Customer or Agent Query] --> H[Validate and Rewrite Query]
        H --> I[Embed Query]
        I --> J[Retrieve Top-K Chunks]
        F --> J
        J --> K[Rank and Filter Context]
        K --> L[Build Prompt]
        L --> M[Generate Answer]
        M --> N[Return Answer, Sources, and Next Action]
    end
```

## Application Architecture Flow

```mermaid
flowchart TD
    A[Frontend Application] --> B[Backend API]

    subgraph Frontend[User Interfaces]
        A1[Customer Chat UI]
        A2[Agent Ticket Console]
    end

    A1 --> A
    A2 --> A

    subgraph Backend[Backend Services]
        B --> C[Authentication and Authorization]
        C --> D[Conversation Manager]
        D --> E[RAG Orchestrator]
        E --> F[Retriever Service]
        E --> G[LLM Service]
        E --> H[Source Citation Service]
        D --> I[Ticket Service]
    end

    subgraph Data[Data Layer]
        F --> J[(Vector Database)]
        I --> K[(Ticket Database)]
        H --> L[(Document Metadata Store)]
        G --> M[LLM Provider]
    end
```

## Knowledge Base Ingestion Flow

```mermaid
flowchart TD
    A[New or Updated Support Content] --> B{Content Type}

    B -- PDF Manual --> C[PDF Loader]
    B -- FAQ Page --> D[HTML or Markdown Loader]
    B -- Policy Document --> E[Document Loader]
    B -- Historical Ticket --> F[Ticket Export Loader]

    C --> G[Extract Text and Metadata]
    D --> G
    E --> G
    F --> G

    G --> H[Remove Noise]
    H --> I[Normalize Formatting]
    I --> J[Create Chunks]
    J --> K[Attach Metadata]
    K --> L[Generate Embeddings]
    L --> M[(Vector Database)]
    M --> N[Index Ready for Retrieval]
```

## Runtime Question Answering Flow

```mermaid
flowchart TD
    A[User Sends Message] --> B[Classify Intent]
    B --> C{Needs Knowledge Retrieval?}

    C -- No --> D[Handle as General Conversation or App Action]
    C -- Yes --> E[Rewrite Query for Search]

    E --> F[Generate Query Embedding]
    F --> G[Search Vector Database]
    G --> H[Retrieve Candidate Chunks]
    H --> I[Filter by Permission, Product, Region, or Customer Type]
    I --> J[Rank Context]
    J --> K{Enough Evidence?}

    K -- No --> L[Ask Follow-Up or Escalate]
    K -- Yes --> M[Build Grounded Prompt]
    M --> N[Generate Answer]
    N --> O[Validate Against Retrieved Sources]
    O --> P{Answer Is Grounded?}

    P -- Yes --> Q[Return Answer with Citations]
    P -- No --> R[Return Safe Fallback or Escalate]
```

## Escalation Flow

```mermaid
flowchart TD
    A[Customer Question] --> B[RAG Assistant Attempts Answer]
    B --> C{Resolved?}

    C -- Yes --> D[Session Closed]
    C -- No --> E[Collect Required Details]
    E --> F[Create Ticket]
    F --> G[Attach Conversation Summary]
    G --> H[Attach Retrieved Sources]
    H --> I[Assign Priority]
    I --> J[Route to Agent Queue]
    J --> K[Agent Reviews Suggested Answer]
    K --> L[Agent Responds to Customer]
```

## Feedback and Continuous Improvement Flow

```mermaid
flowchart TD
    A[Customer or Agent Feedback] --> B{Feedback Type}

    B -- Helpful Answer --> C[Mark Response as Successful]
    B -- Incorrect Answer --> D[Flag for Review]
    B -- Missing Information --> E[Create Knowledge Gap]
    B -- Bad Source --> F[Review Document Metadata]

    C --> G[Analytics Dashboard]
    D --> H[Human Review Queue]
    E --> I[Knowledge Base Update Request]
    F --> J[Index Quality Review]

    H --> K[Improve Prompt, Retrieval, or Documents]
    I --> L[Add or Update Support Content]
    J --> M[Fix Chunking or Source Mapping]

    K --> N[Rebuild or Update Index]
    L --> N
    M --> N
    N --> O[Improved RAG System]
```

## Support Ticket Lifecycle with RAG

```mermaid
stateDiagram-v2
    [*] --> NewTicket
    NewTicket --> RAGAttempt: Customer asks question
    RAGAttempt --> ResolvedBySelfService: Answer accepted
    RAGAttempt --> EscalatedToAgent: Answer rejected or low confidence
    EscalatedToAgent --> AgentReview: Ticket assigned
    AgentReview --> AgentResponded: Agent sends response
    AgentResponded --> WaitingForCustomer
    WaitingForCustomer --> AgentReview: Customer replies
    WaitingForCustomer --> ResolvedByAgent: Customer confirms resolution
    ResolvedBySelfService --> [*]
    ResolvedByAgent --> [*]
```

## Main Components

| Component | Purpose |
| --- | --- |
| Customer Chat UI | Allows customers to ask questions and receive self-service support. |
| Agent Console | Helps support agents review tickets, sources, and suggested responses. |
| Ingestion Pipeline | Loads, cleans, chunks, and embeds support documents. |
| Vector Database | Stores document embeddings for semantic search. |
| Retriever | Finds the most relevant support content for a question. |
| Prompt Builder | Combines the user question with retrieved context. |
| LLM | Generates a natural-language response from the grounded prompt. |
| Citation Service | Shows which documents were used to answer the question. |
| Ticket Service | Creates and manages escalated support tickets. |
| Feedback Loop | Captures quality signals to improve the system over time. |

## Key Design Rules

- Customers should receive simple, direct answers with visible sources when
  useful.
- Agents should receive richer context, similar tickets, policy notes, and a
  draft response they can edit.
- The system should not answer beyond the retrieved knowledge base when the
  question requires company-specific facts.
- Low-confidence or missing-context cases should escalate to a human agent.
- Every generated answer should be traceable to source documents or ticket
  history.

## Example User Journey

```mermaid
sequenceDiagram
    participant Customer
    participant SupportApp
    participant RAG
    participant VectorDB
    participant LLM
    participant Agent

    Customer->>SupportApp: My order was delivered damaged. What should I do?
    SupportApp->>RAG: Send customer question
    RAG->>VectorDB: Search return policy and damaged item process
    VectorDB-->>RAG: Return relevant policy chunks
    RAG->>LLM: Generate grounded answer from policy context
    LLM-->>RAG: Draft response
    RAG-->>SupportApp: Answer with sources and next steps
    SupportApp-->>Customer: Show answer
    Customer->>SupportApp: I still need help
    SupportApp->>Agent: Create ticket with summary and sources
    Agent-->>Customer: Sends personalized response
```

## Success Metrics

- Self-service resolution rate
- Average ticket handling time
- Retrieval relevance score
- Answer faithfulness score
- Escalation rate
- Customer satisfaction score
- Agent edit rate for generated drafts
- Number of identified knowledge gaps

## Suggested Build Order

1. Build document ingestion for FAQs and support articles.
2. Add chunking, embeddings, and vector storage.
3. Build a simple customer chat interface.
4. Add source-backed answer generation.
5. Add escalation to a support ticket.
6. Build the agent console view.
7. Add feedback collection.
8. Add evaluation and monitoring.
9. Improve retrieval with filters, reranking, and better metadata.
