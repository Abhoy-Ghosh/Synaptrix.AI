# 🧠 Synaptrix AI

### Autonomous Multi-Agent Research Intelligence & Cross-Paper Synthesis Platform

<p align="center">

[![Live App](https://img.shields.io/badge/Live%20Demo-synaptrix--ai.vercel.app-00C7B7?style=for-the-badge&logo=vercel&logoColor=white)](https://synaptrix-ai.vercel.app/)
[![API Backend](https://img.shields.io/badge/API%20Endpoint-synaptrix--api.onrender.com-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://synaptrix-api.onrender.com/docs)

![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-FF6F00?style=for-the-badge)
![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash%20%2B%20Groq%20Fallback-8E24AA?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

# 🚀 Overview

**Synaptrix AI** is an autonomous multi-agent research intelligence and cross-paper synthesis platform. Traditional AI tools treat research as isolated summarization tasks—taking one paper at a time or executing naive keyword lookups without retaining context or understanding cross-disciplinary connections.

Synaptrix AI redefines scientific discovery through an agentic pipeline combining **multi-source retrieval (arXiv, Semantic Scholar, IEEE, Springer)**, **dense vector memory (FAISS)**, **tri-signal hybrid ranking**, **dynamic semantic clustering**, **two-tier LLM fallback reasoning**, and **real-time interactive knowledge graphs**.

---

# 🔥 One-Line Pitch

> *“An adaptive research intelligence engine that bridges disconnected literature, uncovers hidden research gaps, and learns what matters over time.”*

---

# 📖 The Engineering Story (In Short)

> *For the complete unabridged technical retrospective with in-depth debugging workflows, read [docs/SYNAPTRIX_ENGINEERING_STORY.md](file:///d:/research-synthesizer/docs/SYNAPTRIX_ENGINEERING_STORY.md).*

### 1. The Spark & The Problem
Most AI paper search tools suffer from three fatal flaws:
1. **The Single-Paper Trap**: They summarize papers independently, missing cross-methodological contradictions and thematic consensus.
2. **Stateless Amnesia**: Every query runs from scratch, ignoring past search context and domain history.
3. **Fragile LLM Pipelines**: Hardcoded dependency on a single model endpoint causes catastrophic failure when rate limits hit.

Synaptrix was built to solve this: an autonomous, memory-backed multi-agent engine that synthesizes literature across papers and learns user relevance over time.

---

### 2. The Architectural Evolution
The system evolved across 4 distinct milestones:
- **Phase 0 — The One-Shot Script**: A CLI-based pipeline querying arXiv and feeding abstracts into a prompt. *Problem: high latency, token waste, zero persistence.*
- **Phase 1 — Embedding & FAISS Vector Memory**: Integrated `all-MiniLM-L6-v2` dense embeddings with normalized in-memory `faiss.IndexFlatIP` cosine similarity and MD5 prompt caching.
- **Phase 2 — Multi-Agent Reasoning Matrix**: Split monolithic prompts into specialized agents (*Retriever*, *Hybrid Ranker*, *Clusterer*, *Summarizer*, *Analyzer*, *Gap Finder*, *Meta-Synthesizer*).
- **Phase 3 — Stateful Intelligence Platform**: Implemented an async FastAPI backend backed by SQLite (`projects` ➔ `chats` ➔ `messages`), Server-Sent Events (SSE) streaming, and an interactive React frontend with Force-Directed Knowledge Graphs and Canvas Analytics.

---

### 3. The 7 Breakthrough Debugging War Stories

| # | Hurdle | Root Cause | Engineering Solution |
|---|---|---|---|
| 🐛 **1** | **RAM Explosion (1.2GB+)** | Multiple modules independently loaded heavyweight 420MB `all-mpnet-base-v2` models. | Standardized on a centralized singleton in `model_loader.py` with `all-MiniLM-L6-v2` (90MB). RAM dropped by **60%**; boot time dropped from 45s to **3s**. |
| 🐛 **2** | **Groq Fallback 404** | Deprecated model ID (`llama-3.1-8b-instant`) in Groq API. | Ran live endpoint introspection; transitioned fallback to **`qwen/qwen3.8-27b`** with zero downtime. |
| 🐛 **3** | **Follow-up Classifier Misrouting** | Overly broad keyword matching (`"compare"`, `"how"`) intercepted complex research queries into shallow chat. | Engineered a strict two-tier classifier: complex queries always trigger full paper retrieval; only pure conversational questions route to lightweight chat. |
| 🐛 **4** | **The Gitignore Cloud Trap** | A generic `cache/` rule in `.gitignore` silently omitted `backend/app/cache/cache.py` from git commits, breaking Docker builds. | Replaced broad patterns with specific path ignores (`backend/app/cache/cache.json`) and added package `__init__.py` files. |
| 🐛 **5** | **Render Free-Tier Disks Policy** | Render Free Tier disallowed persistent disk mounts (`disk:`) in `render.yaml`. | Made database, cache, and index storage gracefully initialize in ephemeral container storage with automated path creation (`os.makedirs`). |
| 🐛 **6** | **CORS Preflight Blocking** | Strict domain matching in FastAPI CORS blocked Vercel cross-origin requests. | Configured comprehensive CORS middleware handling `allow_origin_regex` and credential headers for seamless production API access. |
| 🐛 **7** | **Canvas Analytics Crash** | Backend returned dictionary payloads while frontend Canvas charts expected object arrays. | Implemented robust data normalization on API serialization, preventing UI crashes. |

---

### 4. Cloud Production Deployment
- **Frontend**: Hosted on **Vercel** with optimized Vite production build, automatic client-side SPA routing (`vercel.json`), and custom glassmorphic CSS variables.
- **Backend**: Containerized via **Docker** on **Render**, serving async FastAPI, SSE streaming pipelines, and singleton vector models.

---

# 📚 Table of Contents

- [🚀 Overview](#-overview)
- [🔥 One-Line Pitch](#-one-line-pitch)
- [📖 The Engineering Story (In Short)](#-the-engineering-story-in-short)
- [🎯 Core Vision & Differentiators](#-core-vision--differentiators)
- [🏗️ System Architecture](#️-system-architecture)
- [🤖 Multi-Agent Architecture](#-multi-agent-architecture)
- [⚖️ Hybrid Ranking Engine](#️-hybrid-ranking-engine)
- [🧠 Semantic Clustering & Cross-Paper Synthesis](#-semantic-clustering--cross-paper-synthesis)
- [⚡ Execution Modes](#-execution-modes)
- [✨ Key Platform Features](#-key-platform-features)
- [🧱 Tech Stack](#-tech-stack)
- [📂 Project Directory Structure](#-project-directory-structure)
- [⚙️ Environment Setup & Quickstart](#️-environment-setup--quickstart)
- [🌐 Live Production Deployments](#-live-production-deployments)
- [🐳 Docker & Cloud Deployment](#-docker--cloud-deployment)
- [📦 Multi-Format Research Exports](#-multi-format-research-exports)
- [🎨 UI / UX Philosophy](#-ui--ux-philosophy)
- [🚀 Future Roadmap](#-future-roadmap)
- [👨‍💻 Author & Contributions](#-author--contributions)
- [📜 License](#-license)

---

# 🎯 Core Vision & Differentiators

| Traditional Research Tools | Synaptrix AI Intelligence Engine |
|---|---|
| ❌ Summarize isolated papers one-by-one | ✅ **Cross-Paper Synthesis**: Compares methodologies, detects consensus and contradictions |
| ❌ Pure keyword or naive embedding search | ✅ **Tri-Signal Hybrid Ranking**: Semantic (60%) + Keyword (25%) + Feedback (15%) |
| ❌ Stateless queries without historical memory | ✅ **Relational Research Storage**: Projects, sub-chats, and vector memory |
| ❌ Single LLM vulnerability (rate limits / outages) | ✅ **Two-Tier LLM Fallback**: Gemini 2.0 Flash primary with Groq Qwen fallback |
| ❌ Static text-only report outputs | ✅ **Dynamic Force-Directed Knowledge Graph** & Canvas Analytics |

---

# 🏗️ System Architecture

```
                                  ┌───────────────────────────┐
                                  │   User Research Topic     │
                                  └─────────────┬─────────────┘
                                                │
                                  ┌─────────────▼─────────────┐
                                  │   MD5 Prompt Cache Check  │
                                  └─────────────┬─────────────┘
                                                │ (Cache Miss)
                                  ┌─────────────▼─────────────┐
                                  │  Academic Retriever Agent │
                                  │ (arXiv, S2, IEEE, Springer│
                                  └─────────────┬─────────────┘
                                                │
                                  ┌─────────────▼─────────────┐
                                  │    FAISS Vector Memory    │
                                  │   + Hybrid Ranker Agent   │
                                  └─────────────┬─────────────┘
                                                │
                                  ┌─────────────▼─────────────┐
                                  │ Semantic Clusterer Matrix │
                                  │ (Cosine Distance Dot-Prod)│
                                  └─────────────┬─────────────┘
                                                │
             ┌──────────────────────────────────┼──────────────────────────────────┐
             │                                  │                                  │
    ┌────────▼─────────┐               ┌────────▼─────────┐               ┌────────▼─────────┐
    │ Summarizer Agent │               │  Analyzer Agent  │               │ Gap Finder Agent │
    │ (Core Findings)  │               │ (Methodologies)  │               │ (Open Questions) │
    └────────┬─────────┘               └────────┬─────────┘               └────────┬─────────┘
             │                                  │                                  │
             └──────────────────────────────────┼──────────────────────────────────┘
                                                │
                                       ┌────────▼──────────┐
                                       │ Synthesizer Agent │
                                       │ (Meta-Synthesis)  │
                                       └────────┬──────────┘
                                                │
                                       ┌────────▼──────────┐
                                       │ Output Payload    │
                                       │ ├─ SSE Stream     │
                                       │ ├─ SQLite Persist │
                                       │ └─ Knowledge Graph│
                                       └───────────────────┘
```

---

# 🤖 Multi-Agent Architecture

Synaptrix breaks research synthesis into specialized, autonomous agent modules:

| Agent | Responsibility | Core Implementation |
|---|---|---|
| **Retriever Agent** | Multi-source academic retrieval across arXiv, Semantic Scholar, Springer Nature, and IEEE Xplore. | `backend/app/agents/retriever.py` |
| **Hybrid Ranker** | Re-ranks candidates combining dense cosine similarity, BM25/keyword density, title matching, and user feedback history. | `backend/app/agents/ranker.py` |
| **Clusterer Agent** | Constructs dynamic similarity matrices across document embeddings to identify conceptual groupings. | `backend/app/agents/clusterer.py` |
| **Summarizer Agent** | Generates structured, high-density scientific abstracts without conversational fluff. | `backend/app/agents/summarizer.py` |
| **Analyzer Agent** | Extracts core experimental methodologies, datasets, benchmarks, and performance metrics. | `backend/app/agents/analyzer.py` |
| **Gap Finder Agent** | Detects blind spots, unresolved limitations, and fertile directions for future exploration. | `backend/app/agents/gap_finder.py` |
| **Synthesizer Agent** | Harmonizes all parallel agent findings into an integrated cross-paper meta-synthesis. | `backend/app/agents/synthesizer.py` |
| **Follow-up Agent** | Classifies conversational intent for instant contextual clarification queries. | `backend/app/agents/followup.py` |

---

# ⚖️ Hybrid Ranking Engine

Standard semantic retrieval frequently suffers from semantic drift where conceptually adjacent but practically irrelevant papers score highly. Synaptrix calculates a composite relevance score for each candidate:

$$\text{Final Score} = 0.60 \cdot \mathcal{S}_{\text{semantic}} + 0.25 \cdot \mathcal{S}_{\text{keyword}} + 0.15 \cdot \mathcal{S}_{\text{feedback}} + \mathcal{B}_{\text{title}} + \mathcal{B}_{\text{phrase}}$$

```python
# Hybrid score computation
final_score = (
    0.60 * semantic_similarity
    + 0.25 * keyword_match_score
    + 0.15 * adaptive_feedback_score
    + title_boost
    + phrase_boost
)
```

- **Semantic Similarity (60%)**: Cosine similarity against `all-MiniLM-L6-v2` dense embedding vector.
- **Keyword Alignment (25%)**: Exact token matches across paper title, abstract, and query keywords.
- **Adaptive Reinforcement (15%)**: Historic upvote/downvote signals stored in user feedback tables.
- **Topical Boosts**: High-confidence multipliers for exact phrase matching in paper titles.

---

# 🧠 Semantic Clustering & Cross-Paper Synthesis

Rather than feeding raw abstracts sequentially to an LLM, Synaptrix computes a pairwise cosine similarity matrix:

$$\text{Sim}(D_i, D_j) = \frac{\mathbf{e}_i \cdot \mathbf{e}_j}{\|\mathbf{e}_i\| \|\mathbf{e}_j\|}$$

Papers with similarity above threshold $\tau$ are dynamically clustered into research themes (e.g. *Quantization & Pruning*, *Attention Optimization*, *Hardware Acceleration*). The Synthesizer Agent then reasons over clusters to identify:
1. **Consensus**: Common baseline assumptions shared across all papers.
2. **Methodological Divergence**: Where approaches differ in complexity, latency, or compute overhead.
3. **Contradictions & Outliers**: Discrepancies in experimental findings.

---

# ⚡ Execution Modes

| Mode | Execution Strategy | LLM Latency | Depth & Breadth | Ideal Use Case |
|---|---|---|---|---|
| ⚡ **Fast** | Single-pass combined agent prompt | $\approx 2 - 4\text{s}$ | ⭐⭐⭐ | Rapid literature triage & quick sanity checks |
| 🔀 **Parallel** | Concurrent async agent execution (`asyncio.gather`) | $\approx 4 - 8\text{s}$ | ⭐⭐⭐⭐ | Comprehensive research review with fast turnaround |
| 🔬 **Deep Research** | Multi-stage sequential reasoning & gap analysis | $\approx 10 - 18\text{s}$ | ⭐⭐⭐⭐⭐ | Rigorous survey preparation & meta-analysis |

---

# ✨ Key Platform Features

1. **⚡ Real-Time SSE Streaming**: Live status feedback displaying each agent execution phase in real time.
2. **🧠 Force-Directed Knowledge Graph**: Interactive HTML5 Canvas physics simulation mapping paper nodes (sized by citations) connected by semantic similarity edges.
3. **📊 Pure Canvas Analytics Dashboard**: High-performance dashboard rendering topic distribution donuts, citation timelines, and paper analytics with zero chart library bloat.
4. **🔍 Global Spotlight Search (`Ctrl+K`)**: Instant keyboard-driven modal indexing projects, chats, and stored research messages.
5. **📤 Multi-Format Academic Exports**: One-click generation of:
   - Formatted Academic Markdown (`.md`)
   - BibTeX Citation Library (`.bib`)
   - Branded PDF Research Reports (via ReportLab)
   - Clipboard Ready Summaries
6. **🌙 Adaptive Theme Engine**: Custom dark / light glassmorphism palette persisted to `localStorage`.
7. **🛡️ Resilient Two-Tier LLM Architecture**: Seamless automatic failover between Google Gemini 2.0 Flash and Groq Qwen-3.8-27b.

---

# 🧱 Tech Stack

### Frontend
- **Framework**: React 18 with Vite
- **Animations & Icons**: Lucide React, GSAP, Canvas Physics Engine
- **Styling**: Vanilla CSS3 Custom Properties (Glassmorphic design system)
- **Networking**: EventSource (SSE) + Axios

### Backend & AI
- **Framework**: FastAPI (Async Python 3.11+)
- **Server**: Uvicorn (ASGI)
- **Vector Database**: FAISS (`IndexFlatIP`)
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (Singleton Loader)
- **Primary LLM**: Google Gemini 2.0 Flash (`google.genai`)
- **Fallback LLM**: Groq API (`qwen/qwen3.8-27b`)
- **Database**: SQLite3 (`synaptrix.db`) with WAL mode
- **Report Engine**: ReportLab (Python PDF generation)

---

# 📂 Project Directory Structure

```text
research-synthesizer/
├── backend/
│   ├── app/
│   │   ├── agents/            # Specialized autonomous reasoning agents
│   │   │   ├── retriever.py   # Multi-source paper search
│   │   │   ├── ranker.py      # Tri-signal hybrid ranker
│   │   │   ├── clusterer.py   # Cosine similarity grouping
│   │   │   ├── summarizer.py  # Structured summarization
│   │   │   ├── analyzer.py    # Deep methodological analysis
│   │   │   ├── gap_finder.py  # Research gap detector
│   │   │   ├── synthesizer.py # Cross-paper meta-synthesizer
│   │   │   └── followup.py    # Intent router for conversations
│   │   ├── ai_engine/         # Embeddings & model singleton loaders
│   │   ├── cache/             # Disk & memory query caches
│   │   ├── feedback/          # Relevance learning & scoring
│   │   ├── retrieval/         # arXiv, Semantic Scholar, Springer connectors
│   │   ├── routes/            # FastAPI endpoint routers (chat, search, export)
│   │   ├── services/          # LLM service & two-tier fallback logic
│   │   ├── storage/           # SQLite schema & database queries
│   │   └── main.py            # FastAPI app initialization & CORS setup
│   ├── Dockerfile             # Container configuration
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/        # UI components (KnowledgeGraph, SearchModal, etc.)
│   │   ├── pages/             # Main application views & Dashboard
│   │   ├── services/          # API client & SSE streaming handlers
│   │   ├── App.jsx            # State management & routing
│   │   └── index.css          # Design system & theme tokens
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
│
├── docs/
│   ├── SYNAPTRIX_ENGINEERING_STORY.md  # Complete engineering deep dive
│   ├── deploy.md                       # Cloud deployment guide
│   └── codebase_graph_doc.md           # Architecture visualization guide
│
├── Screenshot/                # Application preview images & UI assets
├── codebase_graph.html        # Interactive codebase neural graph
├── render.yaml                # Render Blueprint deployment specification
└── vercel.json                # Vercel deployment configuration
```

---

# ⚙️ Environment Setup & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/Abhoy-Ghosh/Synaptrix.AI.git
cd Synaptrix.AI
```

### 2. Configure Environment Variables

**Backend (`backend/.env`)**:
```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
SEMANTIC_SCHOLAR_API_KEY=your_optional_s2_key
SPRINGER_META_API_KEY=your_optional_springer_key
IEEE_API_KEY=your_optional_ieee_key
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Frontend (`frontend/.env`)**:
```env
VITE_API_URL=http://localhost:8001
```

---

### 3. Launch the Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Backend will be accessible at `http://localhost:8001` (API Docs: `http://localhost:8001/docs`).

---

### 4. Launch the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will open at `http://localhost:5173`.

---

# 🌐 Live Production Deployments

| Service | Environment | Live URL | Status |
|---|---|---|---|
| **Frontend Web App** | Vercel (Production SPA) | [https://synaptrix-ai.vercel.app](https://synaptrix-ai.vercel.app/) | ![Active](https://img.shields.io/badge/Status-Live-success?style=flat-square) |
| **Backend API (Docs)** | Render (FastAPI Docker) | [https://synaptrix-api.onrender.com/docs](https://synaptrix-api.onrender.com/docs) | ![Active](https://img.shields.io/badge/Status-Live-success?style=flat-square) |
| **API Health Check** | Render Server | [https://synaptrix-api.onrender.com](https://synaptrix-api.onrender.com) | ![Active](https://img.shields.io/badge/Status-Healthy-blue?style=flat-square) |

---

# 🐳 Docker & Cloud Deployment

### Run with Docker
```bash
cd backend
docker build -t synaptrix-backend .
docker run -p 8001:8001 --env-file .env synaptrix-backend
```

### Cloud Production Setup
- **Render Backend**: Configured via `render.yaml` serving `https://synaptrix-api.onrender.com`. For step-by-step instructions, see [docs/deploy.md](file:///d:/research-synthesizer/docs/deploy.md).
- **Vercel Frontend**: Continuous deployment connected to `frontend/` directory at `https://synaptrix-ai.vercel.app/` with `VITE_API_URL=https://synaptrix-api.onrender.com`.

---

# 📦 Multi-Format Research Exports

Synaptrix enables exporting research intelligence directly into academic publishing pipelines:
- **BibTeX (`.bib`)**: Formatted citations including author list, year, journal/arXiv ID, and DOI URLs ready for LaTeX integration.
- **Markdown (`.md`)**: Full report with executive summaries, cluster analysis, and research gap breakdown.
- **PDF Dossier**: Generated server-side using ReportLab with clean typography, metadata headers, and paper tables.

---

# 🎨 UI / UX Philosophy

Synaptrix combines scientific density with high-performance interaction design:
- **Distraction-Free Landing**: Minimalist glassmorphic prompt card with mode selection.
- **Autonomous Pane Transition**: Smoothly morphs into a dual-sidebar workspace upon search submission.
- **Real-Time Visual Diagnostics**: Transparent agent pipeline states and interactive physics-based Knowledge Graph.

---

# 🚀 Future Roadmap

- [ ] **Automated Literature Contradiction Detection**: Semantic sentiment and claim polarity checking across conflicting papers.
- [ ] **Persistent FAISS Indexing**: Multi-tenant cloud vector search with continuous arXiv stream ingestion.
- [ ] **Multi-modal Visual Extraction**: Automated parsing and comparison of figures, tables, and architecture diagrams from paper PDFs.
- [ ] **Zotero & Mendeley Sync**: Direct two-way sync with reference managers.

---

# 👨‍💻 Author & Contributions

Created by **Abhoy Ghosh** ([GitHub Profile](https://github.com/Abhoy-Ghosh)) as an advanced AI systems engineering project exploring multi-agent workflows, vector retrieval, and adaptive intelligence.

Contributions, discussions, and pull requests are warmly welcomed!

---

# 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.
