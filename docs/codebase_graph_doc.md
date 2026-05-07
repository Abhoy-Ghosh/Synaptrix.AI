# 🧠 Graphify Documentation — Research Synthesizer AI

---

## 🎯 Purpose

The Graphify module provides a **visual representation of the system architecture** of the Research Synthesizer AI.

It helps to:

* Understand system flow
* Trace how components interact
* Map code structure to system logic
* Present architecture clearly (demo / README / hackathon)

---

## 🧱 Types of Graphs

### 1️⃣ System Flow Graph

Shows **logical execution flow**:

```
Query → Retriever → Insight → Agents → LLM → Output
```

Used for:

* understanding pipeline
* explaining system behavior

---

### 2️⃣ File Graph

Shows **file-level dependencies**:

```
pipeline.py → retriever.py → llm_service.py
```

Used for:

* debugging
* dependency tracing

---

### 3️⃣ Hybrid Graph (Current Implementation) ✅

Combines both:

```
System Flow  +  Actual Files
```

Example:

```
summarizer → app/agents/summarizer.py
llm_service → app/services/llm_service.py
```

---

## ⚙️ Architecture Representation

### 🔴 Core Flow

* query
* retriever
* insight_extractor
* llm_service
* output

---

### 🔵 Agents

* summarizer
* analyzer
* gap_finder

---

### 🟢 Services

* llm_service
* semantic_service
* arxiv_service

---

### 🟡 Storage

* vector_store (FAISS)
* cache

---

### 💗 Feedback

* feedback_store
* paper_feedback

---

## 🔄 Data Flow

```
User Query
   ↓
Retriever
   ↓
FAISS / Cache
   ↓
Insight Extraction
   ↓
Multi-Agent Processing
   ↓
LLM
   ↓
Final Output
```

---

## 🎨 Graph Legend

| Color     | Meaning     |
| --------- | ----------- |
| 🔴 Red    | System Flow |
| 🔵 Blue   | Agents      |
| 🟢 Green  | Services    |
| 🟡 Yellow | Storage     |
| 💗 Pink   | Feedback    |
| ⚫ Gray    | Other       |

---

## ➡️ Edge Types

* **→ (arrow)** = execution / data flow
* **↘ (mapping)** = file attached to system node

---

## 📁 File Structure Mapping

| System Node  | Files                          |
| ------------ | ------------------------------ |
| retriever    | `app/ai_engine/retriever.py`   |
| summarizer   | `app/agents/summarizer.py`     |
| analyzer     | `app/agents/analyzer.py`       |
| gap_finder   | `app/agents/gap_finder.py`     |
| llm_service  | `app/services/llm_service.py`  |
| vector_store | `app/services/vector_store.py` |
| cache        | `app/cache/cache.py`           |
| feedback     | `app/feedback/*`               |

---

## 🚀 How to Run

```bash
python run_graph.py
```

Output:

```
codebase_graph.html
```

Open:

```bash
xdg-open codebase_graph.html
```

---

## 🧠 Why This Matters

Graphify transforms the project from:

```
Codebase ❌
```

to:

```
Explainable System ✅
```

---

## 🔥 Key Benefits

* Visual debugging
* Architecture clarity
* Faster onboarding
* Demo-ready visualization
* System-level understanding

---

## 🚀 Future Improvements

* Dynamic file detection (auto-mapping)
* Runtime execution tracing
* Interactive filtering (agents/services only)
* Graph-based UI dashboard
* Integration with synthesis layer

---

## 🎯 Summary

Graphify is not just a visualization tool —
it is a **system understanding layer**.

It bridges:

```
Code → Architecture → Intelligence
```

---

## 🧠 Final Insight

> “If you cannot visualize your system, you do not fully understand it.”

---
wslview codebase_graph.html