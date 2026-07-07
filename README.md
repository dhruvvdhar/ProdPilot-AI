# 🚀 ProdPilot AI

> **Enterprise AI-Powered Production Support Platform**
>
> ProdPilot AI is an enterprise-grade AI platform that helps engineers troubleshoot production incidents using Retrieval-Augmented Generation (RAG), Hybrid Search, OCR, and grounded AI responses.

---

# 🚧 Project Status

## Current Development Version

**Version 2.0 (In Progress)**

### ✅ Completed

- Enterprise RAG Pipeline
- Multi-user Backend
- JWT Authentication
- Chat Management APIs
- Hybrid Search (Dense + BM25)
- Cross-Encoder Reranking
- OCR Pipeline with Image Preprocessing
- Evaluation Framework
- Production Benchmarking

### 🚧 Currently Building

- React Frontend
- Docker Containerization
- Responsive Chat Experience
- Production Dashboard

---

# 📖 Overview

ProdPilot AI is an AI-powered Production Support Platform built to assist DevOps Engineers, SREs, Platform Engineers, and Production Support teams during incident investigation.

The platform allows users to upload production artifacts such as:

- Runbooks
- Production Logs
- PDFs
- Architecture Diagrams
- Dashboards
- Screenshots

ProdPilot AI extracts knowledge from these documents, stores it in a vector database, retrieves the most relevant context using Hybrid Search, reranks retrieved documents, and generates grounded responses with citations.

The long-term vision is to evolve ProdPilot AI into an Agentic AI Production Support Platform capable of autonomous investigation and tool execution.

---

# ✨ Features

## AI & RAG

- Retrieval-Augmented Generation (RAG)
- Hybrid Search (Dense + BM25)
- Cross-Encoder Reranking
- Semantic Search
- Prompt Engineering
- Grounded AI Responses
- Context-aware Retrieval
- Source Citations

---

## Document Processing

- PDF Ingestion
- TXT Ingestion
- Log File Ingestion
- OCR-based Image Ingestion
- OpenCV Image Preprocessing
- Architecture Diagram Understanding
- Dashboard Screenshot Understanding

---

## Backend

- FastAPI
- JWT Authentication
- Multi-user Support
- Chat Management
- Conversation History
- Modular Service Architecture
- REST APIs

---

## Evaluation Framework

- LangSmith Evaluation
- Retrieval Evaluation
- Citation Evaluation
- Answer Accuracy Evaluation
- Hallucination Detection
- Latency Benchmarking
- Error Rate Tracking

---

# 🏗 High-Level Architecture

```text
                         User
                           │
                           ▼
                   React Frontend (V2)
                           │
                           ▼
                     FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Authentication      Chat Manager      Upload Manager
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                  Document Ingestion Pipeline
                           │
      ┌──────────────┬──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
     PDF            TXT            Logs          Images
                                                  │
                                                  ▼
                                         OpenCV Preprocessing
                                                  │
                                                  ▼
                                             PaddleOCR
                                                  │
                                                  ▼
                                           Extracted Text
                                                  │
                                                  ▼
                                            Text Chunking
                                                  │
                                                  ▼
                                         Embedding Generation
                                                  │
                                                  ▼
                                           Chroma Vector DB
                                                  │
                      ┌────────────────────────────┴────────────────────────────┐
                      ▼                                                         ▼
                Dense Retrieval                                           BM25 Retrieval
                      │                                                         │
                      └──────────────────────────┬──────────────────────────────┘
                                                 ▼
                                         Hybrid Retriever
                                                 │
                                                 ▼
                                     Cross-Encoder Reranker
                                                 │
                                                 ▼
                                      Context Construction
                                                 │
                                                 ▼
                                       Prompt Engineering
                                                 │
                                                 ▼
                                             Groq LLM
                                                 │
                                                 ▼
                                    Grounded AI Response
                                                 │
                                                 ▼
                                             Citations
```
---

## Detailed Architecture

```text

Refer Folder
 * ProdPilot_Architectures


---

# 📂 Project Structure

```text
ProdPilot-AI/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── evaluation/
│   ├── models/
│   ├── registry/
│   ├── services/
│   ├── storage/
│   ├── utils/
│   └── main.py
│
├── frontend/              (Version 2)
├── documents/
├── tests/
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

---

## AI

- LangChain (LCEL)
- Groq LLM
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering

---

## Retrieval

- Hybrid Search
- Dense Retrieval
- BM25
- Cross-Encoder Reranker

---

## Vector Database

- ChromaDB

---

## OCR

- PaddleOCR
- OpenCV

---

## Evaluation

- LangSmith
- Custom Evaluation Framework

---

## Frontend (Version 2)

- React
- Tailwind CSS

---

## Deployment (Version 2)

- Docker

---

## Future Technologies

- LangGraph
- Kubernetes
- Prometheus
- Grafana
- Cloud Deployment

---

# 📊 Evaluation Results

## Production Benchmark

**40 Production Support Questions**

### Question Categories

| Category            | Count |
|---------------------|------:|
| Single-document     | 18    |
| Cross-document      | 8     |
| Unknown / No-answer | 7     |
| Out-of-scope        | 5     |
| Ambiguous           | 2     |

---

### Runtime

| Metric      | Result |
|-------------|-------:|
| Error Rate  | 0%     |
| P50 Latency | 0.64 s |
| P99 Latency | 4.83 s |

---

### Retrieval Performance

| Metric      | Result |
|-------------|-------:|
| Recall@K    | 86.42% |
| Precision@K | 35.93% |
| Hit Rate    | 92.59% |

---

### Citation Performance

| Metric             | Result |
|--------------------|-------:|
| Citation Recall    | 86.42% |
| Citation Precision | 35.93% |

---

======================================================================
Answer Accuracy Evaluation
======================================================================
Questions : 40
Correct   : 36
Incorrect : 4
Accuracy  : 90.00%


======================================================================
Hallucination Evaluation
======================================================================
Questions             : 40
Grounded Answers      : 37
Hallucinated Answers  : 3
Groundedness Score    : 92.50%
Hallucination Rate    : 7.50%





# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/dhruvvdhar/ProdPilot-AI.git
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Run document ingestion

```bash
python -m tests.test_ingest_documents
```

Run the backend

```bash
python main.py
```

---

# 🗺 Roadmap

## ✅ Version 1

- Enterprise RAG Pipeline
- OCR Support
- Semantic Search
- ChromaDB
- Prompt Engineering

---

## 🚧 Version 2

- Multi-user SaaS Platform
- JWT Authentication
- Chat Management
- React Frontend
- Docker Containerization
- Responsive Chat Experience

---

## 🔜 Version 3

- LangGraph Memory
- Agent Mode
- Tool Calling
- Structured Outputs
- Context Engineering
- Streaming Responses

---

## 🔮 Version 4

Enterprise AI Production Support Platform

- Kubernetes Integration
- Grafana Integration
- Prometheus Integration
- Cloud Deployment
- Observability
- CI/CD Pipelines
- Autonomous Incident Investigation

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Dhruv Dhar**

AI Engineer | Generative AI | Machine Learning | Production AI Systems

Currently building **ProdPilot AI**, an enterprise-grade AI-powered Production Support Platform focused on Retrieval-Augmented Generation (RAG), Hybrid Search, and the future of Agentic AI systems.