# Support Mind: End‑to‑End AI‑Powered Customer Support Copilot

*Published on Medium – November 2026*

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Architecture Overview](#architecture-overview)
3. [Technology Stack](#technology-stack)
4. [Implementation Details](#implementation-details)
    - [Retrieval Pipeline](#retrieval-pipeline)
    - [Agent Graph](#agent-graph)
    - [API Layer](#api-layer)
    - [Mock Order System](#mock-order-system)
5. [Working Process (User Scenarios)](#working-process)
6. [Evaluation](#evaluation)
    - [Agent Behaviour](#agent-behaviour)
    - [Retrieval Quality (RAGAS)](#retrieval-quality)
7. [Challenges & Lessons Learned](#challenges--lessons-learned)
8. [Future Improvements](#future-improvements)
9. [How to Run Locally](#how-to-run-locally)
10. [Conclusion](#conclusion)

---

## Problem Statement <a id="problem-statement"></a>

Businesses often struggle to provide **fast, accurate, and personalized** customer‑support experiences. Traditional ticketing systems require manual triage, and pure‑question‑answer bots frequently give ungrounded answers or lack the ability to **act** on a customer's request (e.g., cancel an order). **Support Mind** aims to create a **deep‑integrated support copilot** that not only answers questions with precise citations but also **resolves tickets end‑to‑end** – looking up order information, cancelling orders, processing refunds, and escalating to a human when needed, while persisting state across restarts.

---

## Architecture Overview <a id="architecture-overview"></a>

```mermaid
flowchart TD
    subgraph UI[User Interface]
        UI1[Web UI (Ask / Resolve tabs)]
    end
    subgraph Agent[LangGraph Resolution Agent]
        AG[Agent Brain – Groq llama‑3.3‑70b‑versatile]
        FALLBACK[Fallback – Gemini‑flash‑lite]
        TOOL_KB[Tool: kb_search (hybrid + rerank)]
        TOOL_ORDER[Tool: order_lookup / cancel / refund]
    end
    subgraph Retrieval[Retrieval Layer]
        CHROMA[ChromaDB + BGE‑small‑en‑v1.5 embeddings]
        BM25[BM25 + Reciprocal Rank Fusion]
        RERANK[Cross‑encoder ms‑marco‑MiniLM‑L‑6‑v2]
    end
    subgraph OMS[Mock Order Management System]
        DB[SQLite + SQLAlchemy]
        SEED[Seeded orders (5% failures injected)]
    end

    UI1 --> AG
    AG --> TOOL_KB
    AG --> TOOL_ORDER
    TOOL_KB --> Retrieval
    TOOL_ORDER --> OMS
    Retrieval --> CHROMA
    Retrieval --> BM25
    Retrieval --> RERANK
    OMS --> DB
    AG --> FALLBACK
```

*Figure 1 – High‑level component diagram of Support Mind.*

The system consists of:
- **FastAPI backend** exposing `/query`, `/chat`, and `/approvals`.
- **LangGraph** orchestrates the agent state graph, handles interruptions for approvals, and persists checkpoints with `SqliteSaver`.
- **Hybrid Retrieval**: dense BGE embeddings + BM25, merged via Reciprocal Rank Fusion (RRF), with optional cross‑encoder reranking.
- **Mock OMS**: a lightweight SQLite database that mimics order lookup, cancellation, and refund flows, with seeded failure scenarios.
- **Human‑in‑the‑loop (HITL)**: refunds above a configurable threshold pause the graph, create an approval record, and resume after a human decision.

---

## Technology Stack <a id="technology-stack"></a>

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Web Framework** | FastAPI |
| **Frontend** | Hand‑crafted HTML/CSS/JS (no React/Gradio) |
| **Agent Engine** | LangGraph (StateGraph, `interrupt`, `SqliteSaver`) |
| **LLMs** | Groq `llama‑3.3‑70b‑versatile` (agent brain) <br> Groq `llama‑3.1‑8b‑instant` (RAG generation) <br> Gemini `gemini‑flash‑lite‑latest` (fallback & eval simulated user) |
| **Embeddings** | `BAAI/bge-small-en-v1.5` |
| **Vector DB** | ChromaDB |
| **Reranker** | `cross‑encoder/ms‑marco‑MiniLM‑L‑6‑v2` |
| **Hybrid Retrieval** | BM25 (`rank‑bm25`) + RRF + optional reranker |
| **Database** | SQLite + SQLAlchemy |
| **Evaluation** | RAGAS (retrieval) + custom scripted scenario harness |
| **CI/CD** | GitHub Actions, Docker, Render (free tier) |

---

## Implementation Details <a id="implementation-details"></a>

### Retrieval Pipeline <a id="retrieval-pipeline"></a>
- **Chunker** (`src/resolveai/ingestion/chunker.py`) splits raw support documents (`data/raw/bitext_support.csv`) into ~200‑token chunks.
- **Vectorstore** (`src/resolveai/ingestion/vectorstore.py`) builds a Chroma collection indexed by BGE embeddings.
- **Hybrid Search** runs a dense similarity search, a BM25 lexical search, and merges results via RRF. When `use_reranker=True`, the top‑k chunks are reranked by the cross‑encoder.
- **Build script**:
  ```bash
  PYTHONPATH=src .venv/bin/python scripts/build_index.py   # ~10 min, one‑time
  ```

### Agent Graph <a id="agent-graph"></a>
- **StateGraph** (`src/resolveai/agent/graph.py`) defines nodes: `ask`, `act`, `guard`, `respond`, `escalate`.
- **Interrupt** creates a checkpoint when a refund exceeds `config.agent.refund_approval_cap`. The checkpoint persists via `SqliteSaver` and is restored after a human POST to `/approvals/{id}`.
- **Tools** (`src/resolveai/agent/tools.py`) wrap the retrieval pipeline (`kb_search`) and the mock OMS client (`order_lookup`, `cancel_order`, `refund_initiate`).
- **Fallback**: If the Groq call fails, the agent retries with Gemini.

### API Layer <a id="api-layer"></a>
- **Routes** (`src/resolveai/api/main.py`):
  - `POST /query` – RAG‑only endpoint.
  - `POST /chat` – Agent‑driven, multi‑turn resolution.
  - `GET/POST /approvals` – Human‑in‑the‑loop approval handling.
- Static files for the UI are mounted under `/`.
- API keys (`GROQ_API_KEY`, `GEMINI_API_KEY`) are read from `.env`.

### Mock Order System <a id="mock-order-system"></a>
- **SQLAlchemy models** (`src/resolveai/orders/models.py`): `Customer`, `Order` with status, amount, and an `idempotency_key` to guarantee exactly‑once refunds.
- **Seeder** (`scripts/seed_orders.py`) creates 50 customers and 200 orders.
- **Failure injection**: 5 % of operations raise `OrderServiceError` to simulate downstream issues.

---

## Working Process (User Scenarios) <a id="working-process"></a>

| Flow | Example Request | Agent Actions | Human Interaction |
|---|---|---|---|
| **Ask (RAG)** | "How do I cancel my order?" | Hybrid retrieval → optional rerank → LLM generates grounded answer with citations. | None |
| **Resolve (Auto)** | "Refund order 8, it arrived damaged" | Intent classification → `refund_initiate` → amount ≤ cap → auto‑approve → reply. | None |
| **Resolve (HITL)** | "Refund order 1, $1 200" (above cap) | Same as above but `interrupt` creates approval record. | Human approves/rejects via `/approvals` UI. |
| **Escalate** | "I want to speak to a human" | Agent routes to `escalate_to_human` tool → returns escalation acknowledgment. | None (agent informs human side‑channel). |

---

## Evaluation <a id="evaluation"></a>

### Agent Behaviour (30 scripted scenarios) <a id="agent-behaviour"></a>

| Metric | Value |
|---|---|
| **Task success rate** | **97 %** (29/30) |
| **Tool‑call accuracy** | **93 %** |
| **Escalation correctness** | **97 %** |
| **Avg turns to resolution** | **1.07** |
| **Grounded‑citation rate (kb_question)** | **75 %** |
| **Avg reply‑quality judge score** | **3.40 / 5** |

Full table is available in `results/agent_eval.md`.

### Retrieval Quality (RAGAS) <a id="retrieval-quality"></a>

| Mode | Reranker | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Rows |
|---|---|---|---|---|---|---|
| semantic | ✘ | 0.85 | 0.70 | 0.90 | 0.84 | 30 |
| hybrid | ✘ | 0.86 | 0.70 | 0.93 | 0.85 | 30 |
| hybrid | ☑ | 0.82 | 0.55 | **1.00** | 0.87 | 30 |

Metrics were generated by `scripts/run_evaluation.py` (see `results/ragas.md`).

#### Observations
- Adding the cross‑encoder **improves context precision to a perfect 1.00** and slightly raises recall, but **faithfulness and answer relevance dip** because the reranker narrows the chunk set, occasionally discarding useful context for the generator.
- The **human‑in‑the‑loop checkpoint** works reliably: after a process restart, the graph resumes from the saved SQLite state (see `tests/test_agent_restart_resume.py`).

---

## Challenges & Lessons Learned <a id="challenges--lessons-learned"></a>

| Challenge | Resolution |
|---|---|
| **Render memory limit (512 MB)** – loading BGE embeddings + reranker exceeded the quota. | Switched to a **smaller quantized model** for local testing and documented the limitation. Production would require a larger instance or lazy‑loading. |
| **Reranker trade‑off** – higher precision but lower faithfulness. | Exposed a **runtime flag** (`use_reranker`) so users can toggle based on latency vs. accuracy preferences. |
| **Idempotency for refunds** – risk of double‑paying when the graph restarts. | Added an **idempotency key** stored in the SQLite checkpoint; the refund tool checks it before executing. |
| **Fail‑fast vs. graceful degradation** – Groq outages required fallback. | Integrated Gemini as a **fallback LLM**; tests simulate failures via the `AgentRuntime` wrapper. |

---

## Future Improvements <a id="future-improvements"></a>

1. **Production‑grade deployment** – migrate to a managed Kubernetes cluster with GPU nodes to host large embedding and reranker models without hitting memory caps.
2. **Quantized / LoRA adapters** – explore 8‑bit quantization for BGE and the cross‑encoder to shrink RAM footprints.
3. **Dynamic chunk size** – adapt chunk length based on token budget, improving relevance for long policy documents.
4. **Real order‑management backend** – replace the mock SQLite store with a micro‑service that talks to an actual ERP/CRM.
5. **Multi‑modal support** – add image‑based troubleshooting (e.g., receipt photos) using Vision LLMs.
6. **Evaluation expansion** – incorporate user‑feedback loops to continually re‑rank the vectorstore based on real interactions.

---

## How to Run Locally <a id="how-to-run-locally"></a>

```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate
PYTHONPATH=src .venv/bin/pip install -r requirements.txt

# Provide API keys
cp .env.example .env   # add GROQ_API_KEY and GEMINI_API_KEY

# Build the retrieval index (once)
PYTHONPATH=src .venv/bin/python scripts/build_index.py

# Start the API + UI
PYTHONPATH=src .venv/bin/python scripts/run_api.py
```

Visit `http://localhost:8000` and try the **Ask** and **Resolve** tabs.

---

## Conclusion <a id="conclusion"></a>

Support Mind demonstrates that a **tight integration of retrieval‑augmented generation with a stateful LangGraph agent** can move beyond simple FAQs to fully automated ticket resolution, complete with human‑in‑the‑loop safeguards. The open‑source repository showcases reproducible evaluation pipelines, durable checkpoints, and a clear separation between retrieval, agent logic, and the mock order domain, making it a solid foundation for extending AI‑driven support in real‑world products.

---

*For the full source code and reproducible results, see the GitHub repository:* https://github.com/Piyush-NST/Support Mind
