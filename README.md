# FinDoc Intelligence — RAG-Powered Financial Document Q&A
**Live Demo:** https://findoc-intelligence-hun8fzasjqqlqgbj5kuojw.streamlit.app
**GitHub:** https://github.com/snehajai907-sys/findoc-intelligence
**Role:** Solo Product Manager — Problem Definition,
           Architecture, Build, Eval, Deployment
**Stack:** Python · Groq (Llama 3.3 70B) · Sentence-Transformers
           · Numpy · Streamlit · LLM-as-Judge Eval

---

## The Problem

Credit analysts and finance professionals spend 3-4 hours
manually reviewing financial documents (loan agreements,
annual reports, earnings releases) to answer specific questions.
The core pain points:

- No way to instantly locate specific clauses or figures
- Manual search misses context buried deep in documents
- Summarisation tools hallucinate numbers — in finance,
  a hallucinated figure creates regulatory and legal exposure
- No confidence signal — users cannot tell if the AI
  is certain or guessing

---

## What I Built

A live RAG (Retrieval-Augmented Generation) system where
a credit analyst uploads any financial document and gets
grounded, cited answers with explicit confidence scores.

The system never guesses. When context is insufficient,
it refuses to answer rather than hallucinating — and skips
the LLM call entirely to save cost.

---

## Architecture Decisions

### RAG over Fine-Tuning
Fine-tuning a model on financial documents requires:
- Labelled Q&A pairs (expensive to create)
- Retraining every time documents change
- Static knowledge that cannot adapt to new filings

RAG retrieves from the actual document at query time.
Zero training cost. Always uses the source of truth.
Perfect for financial documents that change quarterly.

### Chunk Size: 400 Words with 40-Word Overlap
- Below 200 words: fragments clauses, loses context
- Above 600 words: retrieves irrelevant content,
  increases token cost per query
- 40-word overlap: prevents answers split at chunk edges

PM Decision: Chunk size directly affects both accuracy
AND cost. This is an inference cost optimisation decision,
not just an engineering one.

### Numpy over ChromaDB for Vector Search
For single-document Q&A (under 200 chunks), numpy cosine
similarity search is faster than a vector database round-trip
and has zero infrastructure dependencies.
Production path for scale: Pinecone or Weaviate.

### Temperature 0.1 (Not 0.0)
Pure 0.0 causes repetitive phrasing on longer answers.
0.1 adds minimal variation while keeping factual precision
on numerical financial data.

### Structured Output: ANSWER + SOURCE Format
Forces the model to cite its source on every response.
Reduces hallucination risk vs free-form generation
without increasing latency or cost.

---

## Key PM Decisions

### 1. Three-Tier Confidence Gate
| Confidence | Trigger | Action |
|---|---|---|
| HIGH (distance < 0.45) | Strong match found | Answer + citation |
| MEDIUM (distance < 0.70) | Related content found | Answer + caution note |
| LOW (distance ≥ 0.70) | No relevant context | Refuse + skip LLM call |

The LOW confidence gate is the most important product decision.
It prevents hallucination on out-of-scope questions AND
saves token cost by skipping the LLM call entirely.

### 2. Fallback Before LLM Call
When confidence is LOW, the system returns a refusal
message without calling Groq. This means:
- Zero hallucination risk on out-of-scope queries
- Zero token cost on unanswerable questions
- In production at 10,000 queries/month with 30% out-of-scope:
  3,000 LLM calls saved = ~$6/month at GPT-4o pricing

### 3. LLM-as-Judge Evaluation Framework
Rather than manual review or keyword matching (BLEU/ROUGE),
implemented an LLM-as-Judge harness using the same Groq
model to score answers on Groundedness and Relevance.

This scales to thousands of test cases without human
annotation and is more nuanced than n-gram overlap metrics.

---

## Evaluation Results

Ran a 5-question test suite (3 answerable, 2 out-of-scope):

| Metric | Score | Threshold | Status |
|---|---|---|---|
| Avg Groundedness | 1.00 / 1.00 | ≥ 0.80 | ✅ Pass |
| Avg Relevance | 0.83 / 1.00 | ≥ 0.75 | ✅ Pass |
| Fallback Accuracy | 50% | 100% | ⚠️ Needs tuning |
| Hallucinations | 0 / 5 | 0 | ✅ Pass |
| Total Tokens (5 Q) | 1,481 | — | Efficient |

### Eval Finding — Threshold Calibration

The CEO question scored MEDIUM confidence (not LOW)
because generic financial language in the document had
partial semantic overlap with leadership queries.

Root cause: Embedding model sees partial word-level
overlap between financial text and "CEO" query.

PM Decision: Two options evaluated:
1. Tighten CONF_MED from 0.70 → 0.55 (chosen for v1)
2. Add post-retrieval entity-type keyword filter

Chose option 1 — simpler, lower engineering cost.
Even without this fix: zero hallucinations across all
5 tests. The LLM system prompt correctly refused
to fabricate a CEO name despite MEDIUM confidence.

---

## Results & Metrics

| Metric | Value |
|---|---|
| Document processing | Any PDF or TXT, instant indexing |
| Groundedness score | 1.00 / 1.00 (LLM-as-Judge) |
| Relevance score | 0.83 / 1.00 (LLM-as-Judge) |
| Hallucinations | 0 across all test cases |
| Token efficiency | 0 tokens on LOW confidence queries |
| Response time | < 3 seconds per query |
| Deployment | Live on Streamlit Cloud |

---

## What I Would Build Next

1. **PDF table extraction** — Current pypdf misses tabular
   data in structured financial reports. Add pdfplumber
   for table-aware chunking.

2. **Threshold auto-calibration** — Run eval suite on every
   document upload and auto-adjust confidence thresholds
   based on document density and vocabulary.

3. **Multi-document comparison** — Upload two earnings reports
   and ask comparative questions ("How did Q3 margins
   compare to Q2?"). Requires cross-document retrieval logic.

4. **Conversation memory** — Current system is stateless.
   Add session-level conversation history so analysts can
   ask follow-up questions without repeating context.

5. **Audit trail export** — Every Q&A pair with source
   citation exported as a PDF report for compliance teams.

---

## What This Project Demonstrates

| AI PM Competency | How Demonstrated |
|---|---|
| RAG architecture | Chunking → embedding → retrieval → generation |
| LLM selection | Llama 3.3 70B via Groq for speed + cost |
| Prompt engineering | Structured ANSWER+SOURCE format |
| Hallucination handling | Confidence gate + system prompt constraints |
| Human-in-the-Loop | Three-tier confidence display for users |
| LLM Evaluation | LLM-as-Judge (Groundedness + Relevance) |
| Token cost awareness | Fallback skips LLM call — 0 tokens on LOW |
| Edge case thinking | Threshold calibration finding documented |
| Technical deployment | Live on Streamlit Cloud |

---

