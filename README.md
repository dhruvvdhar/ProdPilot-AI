# 🚀 ProdPilot AI

> **AI-Powered Production Support Platform**
>
> An enterprise-grade AI assistant that combines Retrieval-Augmented Generation (RAG) with Agentic AI workflows to help engineers troubleshoot production incidents, retrieve operational knowledge, and automate production support.

---

## 🚧 Project Status

**Current Stable Release:** `v1.0`

✅ Production RAG Assistant Completed

**Currently Developing:** `v2.0`

- Multi-user SaaS Platform
- Authentication & Authorization
- LangGraph Memory
- Chat Management
- React Frontend
- Docker Deployment

---

## 📖 Overview

ProdPilot AI is an AI-powered Production Support platform designed to assist DevOps engineers, SREs, Platform Engineers, and Production Support teams in diagnosing production incidents through natural language conversations.

The platform allows users to upload production artifacts—including runbooks, logs, PDFs, architecture diagrams, and screenshots—and leverages semantic search, vector embeddings, OCR, and Retrieval-Augmented Generation (RAG) to generate grounded, context-aware responses.

Future versions introduce Agentic AI workflows using LangGraph, enabling users to switch between Knowledge Mode (RAG) and Agent Mode for intelligent reasoning, tool calling, and real-time production operations.

---

# ✨ Features

## Version 1.0

- 📄 PDF document ingestion
- 📝 TXT document ingestion
- 📜 Log file ingestion
- 🖼 OCR-based image ingestion
- 🔍 Semantic Search
- 🧠 Retrieval-Augmented Generation (RAG)
- ⚡ LangChain Expression Language (LCEL)
- 🗂 ChromaDB Vector Database
- 🤖 Groq LLM Integration
- 🎯 Grounded AI Responses
- 🏗 Modular Service Architecture

---

## Planned for Version 2

- 🔐 JWT Authentication
- 👤 Multi-user Platform
- 💬 Chat Management
- 🧠 LangGraph Conversation Memory
- 📂 User-specific Document Storage
- 🌐 React Frontend
- 🐳 Docker Deployment
- ⚡ Streaming Responses

---

## Planned for Future Versions

- 🤖 Agent Mode
- 🔧 Tool Calling
- ☸ Kubernetes Integration
- 📈 Grafana Integration
- 📊 Prometheus Integration
- ☁ Cloud Integrations
- 📑 Automated Incident Investigation
- 🔄 Autonomous Production Support Workflows

---

# 🏗 High-Level Architecture

```

                User

                  │

                  ▼

            FastAPI Backend

                  │

                  ▼

         Upload Production Documents

                  │

                  ▼

        Chunking + Embedding Pipeline

                  │

                  ▼

             ChromaDB Vector Store

                  │

                  ▼

           Semantic Retrieval (RAG)

                  │

                  ▼

           Prompt Engineering

                  │

                  ▼

               Groq LLM

                  │

                  ▼

         Grounded AI Response

```

---

# 📂 Project Structure

```

ProdPilot-AI
│
├── app
│ ├── api
│ ├── core
│ ├── services
│ ├── models
│ ├── registry
│ └── main.py
│
├── documents
├── tests
├── requirements.txt
├── README.md
└── LICENSE

```

---

# 🛠 Tech Stack

### Backend

- Python
- FastAPI

### AI / LLM

- LangChain (LCEL)
- Groq LLM
- Prompt Engineering
- Retrieval-Augmented Generation (RAG)

### Vector Database

- ChromaDB

### Embeddings

- Sentence Transformers

### OCR

- PaddleOCR

### Document Processing

- PyPDF
- Pillow

### Future

- LangGraph
- PostgreSQL
- SQLAlchemy
- React
- Docker

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/ProdPilot-AI.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```env
GROQ_API_KEY=your_api_key
```

Run ingestion

```bash
python -m tests.test_ingest_documents
```

Run application

```bash
python main.py
```

---

# 🚀 Roadmap

## ✅ Version 1

- RAG Pipeline
- OCR
- Semantic Search
- ChromaDB
- Prompt Engineering

---

## 🚧 Version 2

- Multi-user SaaS Platform
- Authentication
- LangGraph Memory
- Chat History
- React Frontend
- Docker

---

## 🔮 Version 3

- Agent Mode
- Tool Calling
- Kubernetes
- Grafana
- Prometheus
- Cloud APIs

---

## 🌍 Version 4

Enterprise AI Production Support Platform

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Dhruv Dhar**

AI Engineer | Generative AI | Machine Learning | Production AI Systems

Currently building **ProdPilot AI**, an enterprise AI-powered Production Support Platform.