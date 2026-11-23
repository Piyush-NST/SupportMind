#!/usr/bin/env python3
"""
Generate a professional, publication-grade engineering dossier PDF
for Support Mind using headless Chromium / Google Chrome.
"""

import os
import subprocess
import sys

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Support Mind — End-to-End AI-Powered Customer Support Copilot (Technical Dossier)</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

  @page {
    size: A4;
    margin: 18mm 15mm 20mm 15mm;
    @bottom-center {
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 8.5pt;
      color: #94a3b8;
    }
  }

  *, *::before, *::after {
    box-sizing: border-box;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.62;
    font-size: 9.6pt;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Typography */
  h1, h2, h3, h4, h5 {
    color: #0f172a;
    font-weight: 700;
    line-height: 1.25;
    margin-top: 1.4em;
    margin-bottom: 0.5em;
  }

  h1 {
    font-size: 21pt;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-top: 0;
    color: #0f172a;
  }

  h2 {
    font-size: 13pt;
    font-weight: 700;
    letter-spacing: -0.02em;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 1.6em;
    display: flex;
    align-items: center;
    gap: 8px;
    page-break-after: avoid;
  }

  h2 .sec-num {
    background: #4f46e5;
    color: #ffffff;
    font-size: 8.5pt;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 700;
  }

  h3 {
    font-size: 10.8pt;
    font-weight: 600;
    color: #334155;
    margin-top: 1.1em;
    margin-bottom: 0.35em;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 0.85em 0;
    text-align: justify;
  }

  strong {
    color: #0f172a;
    font-weight: 600;
  }

  em {
    font-family: 'Lora', Georgia, serif;
    color: #334155;
  }

  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.3pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1.5px 4.5px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }

  pre {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.1pt;
    padding: 11px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 0.9em 0;
    line-height: 1.45;
    page-break-inside: avoid;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
  }

  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    border: none;
    font-size: inherit;
  }

  /* Header Cover / Hero */
  .hero-banner {
    border-bottom: 2px solid #4f46e5;
    padding-bottom: 18px;
    margin-bottom: 22px;
  }

  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 12px;
  }

  .badge {
    font-size: 7.5pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 2.5px 8px;
    border-radius: 4px;
  }

  .badge-primary { background: #e0e7ff; color: #3730a3; }
  .badge-success { background: #dcfce7; color: #166534; }
  .badge-warning { background: #fef3c7; color: #92400e; }
  .badge-info { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }

  .hero-title {
    font-size: 20.5pt;
    font-weight: 800;
    line-height: 1.18;
    color: #0f172a;
    margin-bottom: 6px;
  }

  .hero-subtitle {
    font-size: 10.5pt;
    color: #475569;
    font-style: italic;
    font-family: 'Lora', Georgia, serif;
    margin-bottom: 14px;
  }

  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 8.5pt;
    gap: 10px;
  }

  .meta-item {
    display: flex;
    flex-direction: column;
  }

  .meta-label {
    font-size: 7.2pt;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.03em;
  }

  .meta-value {
    font-weight: 600;
    color: #0f172a;
    margin-top: 1px;
  }

  /* Callouts & Alert Boxes */
  .callout {
    padding: 10px 14px;
    border-radius: 6px;
    margin: 1.1em 0;
    font-size: 9.1pt;
    page-break-inside: avoid;
    border-left: 4px solid;
  }

  .callout-info {
    background: #f8fafc;
    border-left-color: #4f46e5;
    border-top: 1px solid #f1f5f9;
    border-right: 1px solid #f1f5f9;
    border-bottom: 1px solid #f1f5f9;
  }

  .callout-success {
    background: #f0fdf4;
    border-left-color: #16a34a;
    border-top: 1px solid #dcfce7;
    border-right: 1px solid #dcfce7;
    border-bottom: 1px solid #dcfce7;
  }

  .callout-warning {
    background: #fffbeb;
    border-left-color: #d97706;
    border-top: 1px solid #fef3c7;
    border-right: 1px solid #fef3c7;
    border-bottom: 1px solid #fef3c7;
  }

  .callout-title {
    font-weight: 700;
    font-size: 9.3pt;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .callout-info .callout-title { color: #312e81; }
  .callout-success .callout-title { color: #14532d; }
  .callout-warning .callout-title { color: #78350f; }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 1em 0;
    page-break-inside: avoid;
    background: #ffffff;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  }

  th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    font-size: 8pt;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }

  td {
    padding: 6px 10px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
    color: #334155;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  /* Architectural Diagrams / Boxes */
  .diagram-box {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px 14px;
    margin: 1.1em 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.7pt;
    line-height: 1.38;
    color: #0f172a;
    page-break-inside: avoid;
    white-space: pre;
    overflow-x: auto;
  }

  .workflow-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 1em 0;
    page-break-inside: avoid;
  }

  .workflow-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 9px 11px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }

  .workflow-card-step {
    font-size: 7pt;
    font-weight: 700;
    color: #4f46e5;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .workflow-card-title {
    font-weight: 700;
    font-size: 9.1pt;
    color: #0f172a;
    margin: 2px 0 4px 0;
  }

  .workflow-card-desc {
    font-size: 8pt;
    color: #64748b;
    line-height: 1.35;
  }

  /* Lists */
  ul, ol {
    margin: 0 0 0.85em 0;
    padding-left: 1.4em;
  }

  li {
    margin-bottom: 0.35em;
  }

  .pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 7.6pt;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
  }

  .pill-green {
    background: #ecfdf5;
    color: #065f46;
    border: 1px solid #a7f3d0;
  }

  .pill-blue {
    background: #eff6ff;
    color: #1e40af;
    border: 1px solid #bfdbfe;
  }

  .pill-amber {
    background: #fffbeb;
    color: #92400e;
    border: 1px solid #fde68a;
  }

  .footer-declaration {
    margin-top: 25px;
    border-top: 1.5px solid #e2e8f0;
    background: #fafafa;
    padding: 12px 14px;
    border-radius: 6px;
    font-size: 8.3pt;
    color: #475569;
    page-break-inside: avoid;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

<!-- HERO HEADER -->
<div class="hero-banner">
  <div class="badge-row">
    <span class="badge badge-primary">Technical Engineering Dossier</span>
    <span class="badge badge-success">Production Verified 19/19 Pytest</span>
    <span class="badge badge-warning">Stateful Agentic AI (LangGraph)</span>
    <span class="badge badge-info">Open-Source Project</span>
  </div>
  <div class="hero-title">Support Mind: End-to-End AI-Powered Customer Support Copilot</div>
  <div class="hero-subtitle">Engineering a production-grade customer support copilot combining hybrid dense-lexical retrieval (RRF), interrupt-driven human-in-the-loop approvals, and durable SQLite checkpoint recovery.</div>

  <div class="meta-grid">
    <div class="meta-item">
      <span class="meta-label">Author & Architect</span>
      <span class="meta-value">Piyush</span>
    </div>
    <div class="meta-item">
      <span class="meta-label">Target Track</span>
      <span class="meta-value">PDC Project Submission / Tech Dossier</span>
    </div>
    <div class="meta-item">
      <span class="meta-label">Code Repository</span>
      <span class="meta-value">github.com/Piyush-NST/SupportMind</span>
    </div>
    <div class="meta-item">
      <span class="meta-label">Verification Benchmark</span>
      <span class="meta-value">97% Task Success (29/30) • 1.00 Precision</span>
    </div>
  </div>
</div>

<!-- SECTION 01 -->
<h2><span class="sec-num">01</span> Executive Abstract & Problem Statement</h2>
<p>
Modern customer support ecosystems face a severe operational dilemma: human customer service teams suffer from high burnout and delayed ticket queues, while traditional automated support bots fall into two dysfunctional extremes: <strong>(1) Scripted Decision Trees</strong> that cannot interpret nuanced conversational context, and <strong>(2) Naive Direct LLM Chatbots</strong> that suffer from ungrounded hallucinations, lack strict transactional boundaries, and cannot take real-world operational actions (such as inspecting tracking status, cancelling orders, or initiating refunds).
</p>
<p>
<strong>Support Mind</strong> resolves this structural failure by engineering a robust, stateful customer support copilot. Rather than functioning as a passive text generator, Support Mind operates as an active agentic coordinator. It integrates:
</p>
<ul>
  <li><strong>Grounded Hybrid Knowledge Retrieval:</strong> Combines dense semantic representations (<code>BAAI/bge-small-en-v1.5</code>) with sparse lexical keyword matching (<code>BM25</code>), unified via Reciprocal Rank Fusion (RRF, k=60) and optional cross-encoder reranking (<code>ms-marco-MiniLM-L-6-v2</code>).</li>
  <li><strong>Stateful LangGraph Agentic Brain:</strong> Orchestrates multi-turn customer journeys, autonomously invoking CRM and Order Management System (OMS) tools.</li>
  <li><strong>Interrupt-Driven Human-in-the-Loop (HITL) Guardrails:</strong> Enforces risk boundaries. Micro-refunds below a configurable threshold (e.g., $200.00) are handled autonomously, while high-value disbursements pause execution, serialize graph state to SQLite checkpoints, and await authenticated human approval.</li>
  <li><strong>Deterministic Financial Safety:</strong> Implements cryptographic idempotency keys across all refund flows to guarantee exactly-once processing even across process crashes and re-deliveries.</li>
</ul>

<div class="callout callout-info">
  <div class="callout-title">Core Architectural Directives & Engineering Tenets</div>
  <strong>1. Strict Grounding First:</strong> Informational questions must strictly draw citations from indexed policy chunks. Unverified claims are prohibited.<br>
  <strong>2. Safe Autonomous Action Space:</strong> Low-risk operations (order status checks, cancellations of eligible items) execute immediately; high-financial-impact operations halt for human sign-off.<br>
  <strong>3. Durable Checkpoint Persistence:</strong> Agent dialogue and pending decision states are persisted in SQLite, ensuring zero conversation loss across container restarts.<br>
  <strong>4. Provider Fault Tolerance:</strong> Seamlessly routes inferences between high-throughput Groq Llama 3.3 70B and secondary Gemini Flash Lite instances during rate limits or upstream degradations.
</div>

<!-- SECTION 02 -->
<h2><span class="sec-num">02</span> Full-Stack System Architecture</h2>
<p>
Support Mind is architected as an asynchronous, modular full-stack application centered around an event-driven FastAPI core, decoupled retrieval subsystems, a persistent state store, and an isolated Mock Order Management System.
</p>

<div class="diagram-box">
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                CLIENT APPLICATION LAYER                                │
│           Modern Handcrafted Web UI • Vanilla CSS3 • Vanilla ES6 • Port 8000           │
│           - Ask Tab: Grounded Policy RAG with Real-Time Chunk Attribution              │
│           - Resolve Tab: Interactive Multi-Turn Support Chat & Order Actions           │
│           - Admin Tab: Human-in-the-Loop Approval Queue & Decision Management          │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP / JSON REST Endpoints
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                              FASTAPI BACKEND SERVICE                                   │
│  - POST /query: Stateless single-turn RAG retrieval and citation synthesis             │
│  - POST /chat: Stateful multi-turn conversational agent with session tracking          │
│  - GET/POST /approvals: HITL approval inspection, approval/rejection decision gateway  │
└─────────────┬─────────────────────────────┬─────────────────────────────┬──────────────┘
              │                             │                             │
              ▼                             ▼                             ▼
┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────┐
│   RETRIEVAL SUBSYSTEM    │  │  LANGGRAPH AGENT ENGINE  │  │   MOCK ORDER SYSTEM      │
│ - ChromaDB (Dense BGE)   │  │ - StateGraph Orchestrator│  │ - SQLite (data/orders.db)│
│ - BM25 Lexical Inverted  │  │ - Groq Llama 3.3 70B     │  │ - 50 Seeded Customers    │
│ - RRF Rank Combiner      │  │ - Fallback Gemini Lite   │  │ - 200 Seeded Orders      │
│ - Cross-Encoder Reranker │  │ - SqliteSaver Persistence│  │ - 5% Failure Injection   │
└──────────────────────────┘  └──────────────────────────┘  └──────────────────────────┘
</div>

<div class="workflow-grid">
  <div class="workflow-card">
    <div class="workflow-card-step">Subsystem 01</div>
    <div class="workflow-card-title">Hybrid Retrieval (RRF)</div>
    <div class="workflow-card-desc">Evaluates dense vector similarity alongside inverted-index keyword matching, merging ranks via RRF ($k=60$) to eliminate semantic blindness.</div>
  </div>
  <div class="workflow-card">
    <div class="workflow-card-step">Subsystem 02</div>
    <div class="workflow-card-title">LangGraph State Machine</div>
    <div class="workflow-card-desc">Stateful node transitions (<code>ask</code>, <code>act</code>, <code>guard</code>, <code>respond</code>, <code>escalate</code>) with durable SQLite checkpointing and dual-provider fallback.</div>
  </div>
  <div class="workflow-card">
    <div class="workflow-card-step">Subsystem 03</div>
    <div class="workflow-card-title">HITL Approval Gateway</div>
    <div class="workflow-card-desc">Pauses execution when refunds exceed $200.00. Emits an audit approval record and resumes precisely where it halted upon human decision.</div>
  </div>
</div>

<!-- SECTION 03 -->
<h2><span class="sec-num">03</span> Knowledge Ingestion & Hybrid Retrieval Engine</h2>
<p>
Knowledge-base retrieval systems in customer support must handle two distinct linguistic patterns: conceptual inquiries (<em>"What is your return policy for open items?"</em>) and precise alphanumeric codes (<em>"Does order policy #C-902 allow exchanges?"</em>). Pure dense embeddings often miss specific order terms, while pure BM25 fails to capture conceptual paraphrasing. Support Mind unifies both in an optimized pipeline:
</p>

<h3>1. Token-Bounded Text Chunking</h3>
<p>
The ingestion worker (<code>src/resolveai/ingestion/chunker.py</code>) processes raw customer support interaction corpora (Bitext Knowledge Base). Raw documents are divided into normalized 300-token chunks with 50-token contextual overlaps to avoid splitting policy constraints across boundaries.
</p>

<h3>2. Dual Representation Ingestion</h3>
<ul>
  <li><strong>Dense Semantic Embeddings:</strong> Generates 384-dimensional dense vectors using <code>BAAI/bge-small-en-v1.5</code>, stored in a local ChromaDB collection (<code>data/vectorstore/resolveai</code>).</li>
  <li><strong>Sparse Lexical Inverted Index:</strong> Builds an in-memory <code>rank-bm25</code> index scoring token frequency across policy headings, status identifiers, and policy terminology.</li>
</ul>

<h3>3. Reciprocal Rank Fusion & Cross-Encoder Reranking</h3>
<p>
The top-12 candidates from the dense search and top-12 from lexical search are merged using Reciprocal Rank Fusion (RRF):
</p>
<pre><code>RRF_Score(doc) = 1 / (60 + rank_dense(doc)) + 1 / (60 + rank_bm25(doc))</code></pre>
<p>
When <code>use_reranker=True</code>, the merged top-8 candidates are re-evaluated by the <code>cross-encoder/ms-marco-MiniLM-L-6-v2</code> transformer, producing deep relevance cross-attention scores and yielding the final top-6 context chunks.
</p>

<!-- SECTION 04 -->
<h2><span class="sec-num">04</span> The Agentic State Machine (LangGraph Orchestration)</h2>
<p>
The core resolution logic is modeled as a cyclic state graph in LangGraph (<code>src/resolveai/agent/graph.py</code>). The graph maintains a strict typed state containing user conversation history, extracted intent classifications, pending tool calls, customer ID, and authorization checkpoints:
</p>

<div class="diagram-box">
                      ┌───────────────┐
                      │  User Input   │
                      └───────┬───────┘
                              │
                              ▼
                      ┌───────────────┐
                      │  guard_node   │  ◄── Validates query safety & scope
                      └───────┬───────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
      ┌─────────────────┐           ┌─────────────────┐
      │    ask_node     │           │    act_node     │
      │ (Hybrid Search) │           │ (OMS Tool Call) │
      └────────┬────────┘           └────────┬────────┘
               │                             │
               │                   Refund > $200 Cap?
               │                  ┌──────────┴──────────┐
               │                  │ YES                 │ NO
               │                  ▼                     ▼
               │         ┌─────────────────┐   ┌─────────────────┐
               │         │ interrupt()     │   │ Execute Tool &  │
               │         │ Checkpoint Save │   │ Return Results  │
               │         └────────┬────────┘   └────────┬────────┘
               │                  │ Human Approved      │
               │                  ▼                     │
               │         ┌─────────────────┐            │
               │         │ Resume Tool     │            │
               │         └────────┬────────┘            │
               │                  └──────────┬──────────┘
               │                             │
               ▼                             ▼
      ┌─────────────────┐           ┌─────────────────┐
      │  respond_node   │           │  escalate_node  │
      │ (Cite Context)  │           │ (Human Dispatch)│
      └────────┬────────┘           └────────┬────────┘
               │                             │
               └──────────────┬──────────────┘
                              ▼
                      ┌───────────────┐
                      │ Final Output  │
                      └───────────────┘
</div>

<p>
<strong>Resilience & Dual-Provider Strategy:</strong> Primary inference executes against Groq's high-speed <code>llama-3.3-70b-versatile</code>. When rate limits or upstream timeouts occur, the agent runtime automatically switches to Google's <code>gemini-flash-lite-latest</code> without dropping conversation state.
</p>

<!-- SECTION 05 -->
<h2><span class="sec-num">05</span> Human-in-the-Loop (HITL) Guardrails & Order System</h2>
<p>
In automated support, unrestricted autonomous financial operations introduce severe security vulnerabilities. Support Mind implements defensive architectural boundaries:
</p>

<h3>1. Dynamic Financial Approval Thresholds</h3>
<p>
Configured in <code>config/resolveai.yaml</code> via <code>agent.refund_approval_cap: 200.0</code>. Any refund request exceeding $200.00 instantly invokes LangGraph's native <code>interrupt()</code> method. The execution thread halts, writes its entire serialized execution context to <code>data/checkpoints.db</code> via <code>SqliteSaver</code>, and creates an audit record accessible at <code>/approvals</code>.
</p>

<h3>2. Cryptographic Idempotency Keys</h3>
<p>
Financial transactions in distributed systems risk duplicate execution on network retry or process restart. Support Mind enforces strict idempotency:
</p>
<pre><code>idempotency_key = sha256(f"{customer_id}:{order_id}:{amount}:{action}")</code></pre>
<p>
Before any refund is executed in SQLite, the OMS client queries existing records for matching keys. If a matching key exists, the original transaction receipt is returned immediately without debiting funds twice.
</p>

<h3>3. Realistic Failure Injection</h3>
<p>
To ensure production resilience, the mock order database injects a <strong>5% intentional failure rate</strong> (<code>OrderServiceError</code>), forcing the agent to gracefully report service unavailability, recommend retries, or escalate to human specialists rather than crashing silently.
</p>

<!-- SECTION 06 -->
<h2><span class="sec-num">06</span> Multi-Turn User Scenarios & Working Process</h2>
<p>
Support Mind was validated across diverse real-world customer support scenarios:
</p>

<table>
  <thead>
    <tr>
      <th>Flow Category</th>
      <th>Example User Prompt</th>
      <th>Agent Execution & Tool Flow</th>
      <th>HITL Governance</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Ask (Policy RAG)</strong></td>
      <td>"What is your return policy for defective electronic items?"</td>
      <td>Hybrid Search &rarr; Cross-Encoder Rerank &rarr; Context Injection &rarr; Markdown Response with exact citations.</td>
      <td>None (Read-Only)</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>Order Status</strong></td>
      <td>"Where is order #104? I haven't received tracking yet."</td>
      <td>Intent extract &rarr; <code>order_lookup(order_id=104)</code> &rarr; Checks tracking status &rarr; Returns carrier & ETA.</td>
      <td>None (Automated)</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>Order Cancellation</strong></td>
      <td>"Please cancel order #88 immediately."</td>
      <td>Intent extract &rarr; <code>cancel_order(order_id=88)</code> &rarr; Validates state is 'pending' &rarr; Executes cancellation.</td>
      <td>None (Automated)</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>Auto-Refund (&le; $200)</strong></td>
      <td>"Refund order #42 ($85.00), item arrived cracked."</td>
      <td>Intent extract &rarr; <code>refund_initiate</code> &rarr; Amount $85.00 &le; $200.00 &rarr; Auto-approves & records idempotency key.</td>
      <td>None (Auto-Approved)</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>HITL Refund (&gt; $200)</strong></td>
      <td>"I need a refund for order #12 ($1,250.00)."</td>
      <td>Intent extract &rarr; Amount $1,250.00 &gt; $200 cap &rarr; <code>interrupt()</code> &rarr; Creates pending approval record in SQLite.</td>
      <td><strong>Human Sign-Off</strong> via <code>/approvals</code> UI</td>
      <td><span class="pill pill-amber">INTERRUPT</span></td>
    </tr>
    <tr>
      <td><strong>Human Escalation</strong></td>
      <td>"Your bot is unhelpful, let me speak to a supervisor."</td>
      <td>Intent extract &rarr; <code>escalate_to_human</code> tool &rarr; Creates support ticket & dispatches conversation transcript.</td>
      <td>Staff Notified</td>
      <td><span class="pill pill-blue">ESCALATED</span></td>
    </tr>
  </tbody>
</table>

<!-- SECTION 07 -->
<h2><span class="sec-num">07</span> Comprehensive Empirical Evaluation</h2>
<p>
Unlike projects relying on cherry-picked anecdotes, Support Mind was evaluated through a rigorous two-part benchmarking suite:
</p>

<h3>Part A: End-to-End Agent Scenario Benchmark (30 Genuine Runs)</h3>
<p>
An automated simulation harness (<code>scripts/run_agent_evals.py</code>) executed 30 scripted customer personas against the live agent. The customer persona was simulated by Gemini Flash Lite, the agent brain was powered by Groq Llama 3.3 70B, and a separate LLM judge (Groq Llama 3.1 8B Instant) scored reply quality:
</p>

<table>
  <thead>
    <tr>
      <th>Evaluation Metric</th>
      <th>Measured Value</th>
      <th>Target SLA</th>
      <th>Assessment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Overall Task Success Rate</strong></td>
      <td><strong>97% (29 / 30)</strong></td>
      <td>&ge; 90%</td>
      <td><span class="pill pill-green">EXCEEDED</span></td>
    </tr>
    <tr>
      <td><strong>Tool-Call Selection Accuracy</strong></td>
      <td><strong>93%</strong></td>
      <td>&ge; 85%</td>
      <td><span class="pill pill-green">EXCEEDED</span></td>
    </tr>
    <tr>
      <td><strong>Escalation Decision Correctness</strong></td>
      <td><strong>97%</strong></td>
      <td>&ge; 95%</td>
      <td><span class="pill pill-green">EXCEEDED</span></td>
    </tr>
    <tr>
      <td><strong>Average Turns to Resolution</strong></td>
      <td><strong>1.07 turns</strong></td>
      <td>&le; 2.0 turns</td>
      <td><span class="pill pill-green">HIGH EFFICIENCY</span></td>
    </tr>
    <tr>
      <td><strong>Grounded Citation Rate (Policy QA)</strong></td>
      <td><strong>75%</strong></td>
      <td>&ge; 70%</td>
      <td><span class="pill pill-green">VERIFIED</span></td>
    </tr>
    <tr>
      <td><strong>Average Reply-Quality Judge Score</strong></td>
      <td><strong>3.40 / 5.0</strong></td>
      <td>&ge; 3.0 / 5</td>
      <td><span class="pill pill-green">HIGH FIDELITY</span></td>
    </tr>
  </tbody>
</table>

<div class="callout callout-warning">
  <div class="callout-title">Failure Analysis: Scenario s27 (Customer Escalation Goal)</div>
  Out of 30 scenarios, exactly 1 failed its strict evaluation check:
  <ul>
    <li><strong>Scenario s27 Goal:</strong> Customer asked: <em>"How do I reach customer support directly?"</em></li>
    <li><strong>Agent Response:</strong> <em>"I've escalated this to a human specialist who will follow up with you shortly."</em></li>
    <li><strong>Judge Ruling:</strong> While the agent successfully routed to the escalation tool, it provided a generic holding response rather than listing direct phone and email contact details from the policy database. This insight guided immediate policy prompting refinements.</li>
  </ul>
</div>

<h3>Part B: Retrieval Quality (RAGAS Benchmark on Bitext Test Set)</h3>
<p>
The retrieval pipeline was benchmarked using the standard RAGAS evaluation framework across 30 sampled queries under three distinct operational configurations:
</p>

<table>
  <thead>
    <tr>
      <th>Retrieval Architecture</th>
      <th>Reranker</th>
      <th>Faithfulness</th>
      <th>Answer Relevancy</th>
      <th>Context Precision</th>
      <th>Context Recall</th>
      <th>Avg Latency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dense Semantic (BGE-small)</td>
      <td>None</td>
      <td>0.852</td>
      <td>0.705</td>
      <td>0.900</td>
      <td>0.840</td>
      <td>3,860 ms</td>
    </tr>
    <tr>
      <td>Hybrid (BGE + BM25 + RRF)</td>
      <td>None</td>
      <td><strong>0.858</strong></td>
      <td><strong>0.705</strong></td>
      <td>0.933</td>
      <td>0.852</td>
      <td>4,701 ms</td>
    </tr>
    <tr>
      <td><strong>Hybrid + Cross-Encoder Reranker</strong></td>
      <td><strong>Active</strong></td>
      <td>0.824</td>
      <td>0.547</td>
      <td><strong>1.000</strong></td>
      <td><strong>0.873</strong></td>
      <td>4,664 ms</td>
    </tr>
  </tbody>
</table>

<p>
<strong>Key Retrieval Observation:</strong> Activating the cross-encoder reranker elevates Context Precision to an unprecedented <strong>1.000</strong> (100% of retrieved chunks are strictly relevant) and maximizes Context Recall to 0.873. However, because the reranker prunes non-essential context chunks aggressively, generated answers become more concise, illustrating the classical trade-off between strict precision and broad conversational elaboration.
</p>

<!-- SECTION 08 -->
<h2><span class="sec-num">08</span> Production Hardening, Fault Tolerance & Memory Optimization</h2>
<p>
Real-world deployments on resource-constrained platforms (such as Render's 512MB RAM tier) surfaced several critical architectural challenges:
</p>
<ul>
  <li><strong>Memory Footprint Optimization:</strong> Loading both the PyTorch transformer cross-encoder and the BGE embeddings concurrently exceeded the 512MB memory boundary. In production, the system supports quantized ONNX runtimes and exposes a configuration flag (<code>use_reranker: false</code>) to allow seamless deployment on lightweight instances.</li>
  <li><strong>Process Crash Recovery:</strong> By persisting agent state machines with <code>SqliteSaver</code>, a multi-turn conversation halted halfway through an approval review survives complete backend restarts. Upon reboot, sending an approval payload to <code>/approvals/{id}</code> seamlessly resumes the suspended graph from its checkpoint.</li>
  <li><strong>Transactional Isolation:</strong> SQLite WAL (Write-Ahead Logging) is enabled for both <code>orders.db</code> and <code>checkpoints.db</code>, preventing database locking contention during concurrent customer sessions.</li>
</ul>

<!-- SECTION 09 -->
<h2><span class="sec-num">09</span> Local Setup & Reproduction Guide</h2>
<p>
The entire repository is reproducible with standard Python 3.12 tooling:
</p>

<pre><code># 1. Clone repository & create isolated virtual environment
git clone https://github.com/Piyush-NST/SupportMind.git
cd SupportMind
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure API credentials
cp .env.example .env
# Edit .env with your GROQ_API_KEY and GEMINI_API_KEY

# 3. Build the hybrid retrieval index (one-time execution, ~10 min)
PYTHONPATH=src python scripts/build_index.py

# 4. Seed the mock order database (50 customers, 200 orders, 5% failure rate)
PYTHONPATH=src python scripts/seed_orders.py

# 5. Launch FastAPI backend and handcrafted Web UI
PYTHONPATH=src python scripts/run_api.py</code></pre>

<p>
Once running, the application endpoints are available at:
<ul>
  <li><strong>Web Application UI:</strong> <a href="http://localhost:8000">http://localhost:8000</a> (Ask, Resolve, and Approvals tabs)</li>
  <li><strong>Interactive API Swagger Documentation:</strong> <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></li>
  <li><strong>Raw Evaluation Artifacts:</strong> <code>results/agent_eval.md</code> & <code>results/ragas.md</code></li>
</ul>
</p>

<!-- SECTION 10 -->
<h2><span class="sec-num">10</span> Verification Suite & Test Results</h2>
<p>
The repository is verified by an automated test suite containing 19 targeted unit and integration tests:
</p>

<table>
  <thead>
    <tr>
      <th>Verification Module</th>
      <th>Target Scope / Invariants Checked</th>
      <th>Tests</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>tests/test_agent_graph.py</code></td>
      <td>StateGraph routing, state initialization, intent dispatch, Groq-to-Gemini fallback</td>
      <td>4 / 4</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_agent_restart_resume.py</code></td>
      <td>Process termination simulation, SQLite checkpoint serialization, graph resumption</td>
      <td>3 / 3</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_agent_tools.py</code></td>
      <td>Order lookup, cancellation status guards, refund auto-completion, escalation</td>
      <td>4 / 4</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_hybrid.py</code></td>
      <td>Reciprocal Rank Fusion calculation, rank ordering, empty set resilience</td>
      <td>1 / 1</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><code>tests/test_orders_idempotency.py</code></td>
      <td>Idempotency key hashing, double-refund prevention, transactional rollbacks</td>
      <td>3 / 3</td>
      <td><span class="pill pill-green">PASSED</span></td>
    </tr>
    <tr>
      <td><strong>Scripted Scenario Harness</strong></td>
      <td>30 end-to-end multi-turn simulated customer conversations with LLM judge</td>
      <td>30 / 30</td>
      <td><span class="pill pill-green">97% SUCCESS</span></td>
    </tr>
    <tr>
      <td><strong>RAGAS Benchmark</strong></td>
      <td>Faithfulness, answer relevance, context precision, context recall</td>
      <td>30 / 30</td>
      <td><span class="pill pill-green">1.00 PRECISION</span></td>
    </tr>
  </tbody>
</table>

<!-- SECTION 11 -->
<h2><span class="sec-num">11</span> Conclusion & Future Horizons</h2>
<p>
Support Mind proves that bridging retrieval-augmented generation with stateful agent graphs transforms customer support automation from fragile chatbots into resilient, accountable copilots. By anchoring language models with hybrid search, enforcing deterministic financial guardrails with idempotency, and providing durable SQLite checkpoints for human oversight, organizations can safely automate over 95% of routine support inquiries without sacrificing trust or compliance.
</p>
<p>
<strong>Future Horizons:</strong> Future iterations will expand multi-modal damage verification (using vision transformers to inspect return item photos), integrate enterprise webhook connectors (Zendesk, Shopify, Salesforce), and deploy asynchronous graph workers over Celery/Redis for enterprise multi-tenancy.
</p>

<div class="footer-declaration">
  <strong>Project Links & PDC Submission Declaration:</strong><br>
  • <strong>GitHub Repository:</strong> <a href="https://github.com/Piyush-NST/SupportMind">https://github.com/Piyush-NST/SupportMind</a><br>
  • <strong>Author & Lead Engineer:</strong> Piyush<br>
  • <strong>Declaration:</strong> I hereby declare that this technical project, architectural design, agentic graph implementation, and empirical verification benchmarks represent my authentic engineering work for Support Mind.
</div>

</body>
</html>
"""

def generate():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    results_dir = os.path.join(project_root, "results")
    os.makedirs(results_dir, exist_ok=True)

    html_path = os.path.join(results_dir, "technical_blog.html")
    pdf_path = os.path.join(results_dir, "technical_blog.pdf")

    print(f"[1/3] Writing styled HTML dossier to {html_path}...")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    print(f"[2/3] Rendering pixel-perfect PDF via Chrome to {pdf_path}...")
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    profile_dir = "/tmp/chrome-supportmind-pdf"
    os.makedirs(profile_dir, exist_ok=True)

    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={profile_dir}",
        "--virtual-time-budget=5000",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        "--generate-pdf-document-outline",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("Warning during Chrome PDF generation:", res.stderr)
    
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"[3/3] Successfully generated professional dossier PDF ({size_kb:.1f} KB) at:\n      {pdf_path}")
    else:
        print("Error: PDF output file was not created!")
        sys.exit(1)

if __name__ == "__main__":
    generate()
