# ============================================================
# FINDOC INTELLIGENCE — File 1: RAG Pipeline
# PM Purpose: This is the core intelligence layer.
# Every function = one PM decision about accuracy vs speed.
# ============================================================

import os
import re
from groq import Groq
from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

# ─── CONFIGURATION ──────────────────────────────────────────
# PM Decision Log: Every number here is a deliberate choice
CHUNK_SIZE    = 400   # words per chunk
CHUNK_OVERLAP = 40    # overlap between chunks
TOP_K         = 3     # chunks retrieved per query
MODEL         = "llama-3.3-70b-versatile"

# Confidence thresholds (cosine distance scale: 0=identical)
CONF_HIGH = 0.45   # below this = high confidence
CONF_MED  = 0.70   # below this = medium confidence
                   # above 0.70 = low → fallback triggered

# ─── DOCUMENT LOADING ───────────────────────────────────────
def load_document(file_path: str) -> str:
    """
    Load text from PDF or TXT.
    PM Note: Supporting both covers 90% of financial doc
    types without adding complex parsing overhead.
    """
    path = str(file_path)
    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        text   = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
    else:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    return re.sub(r'\s+', ' ', text).strip()


# ─── CHUNKING ───────────────────────────────────────────────
def chunk_text(text: str) -> list:
    """
    Split document into overlapping word-based chunks.

    PM Decision: 400 words (~500 tokens) with 40-word overlap.
    - < 200 words: loses clause context, fragments answers
    - > 600 words: retrieves irrelevant content, higher cost
    - Overlap prevents answers split across chunk boundaries
    """
    words  = text.split()
    chunks = []
    i      = 0
    while i < len(words):
        chunk = " ".join(words[i : i + CHUNK_SIZE])
        if chunk:
            chunks.append(chunk)
        i += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


# ─── VECTOR STORE ───────────────────────────────────────────
def build_vector_store(chunks: list, doc_name: str):
    """
    Embed chunks and store in ChromaDB.

    PM Decision: ChromaDB (local) vs Pinecone (cloud).
    - Free, zero latency, no API key for prototype
    - Production path: Pinecone for persistence + scale
    """
    ef     = SentenceTransformerEmbeddingFunction(
                 model_name="all-MiniLM-L6-v2"
             )
    client = chromadb.Client()

    # Sanitise collection name for ChromaDB rules
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', doc_name)[:40]
    safe_name = safe_name.strip('_') or "findoc"
    if len(safe_name) < 3:
        safe_name = "doc_" + safe_name

    try:
        client.delete_collection(safe_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=safe_name,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)
    return collection


# ─── RETRIEVAL ──────────────────────────────────────────────
def retrieve_context(query: str, collection) -> tuple:
    """
    Retrieve top-k most relevant chunks.

    PM Decision: TOP_K = 3
    - k=1: too narrow, misses complementary context
    - k=5: dilutes answer, raises token cost per query
    - k=3: optimal for single-document financial Q&A
    """
    n = min(TOP_K, collection.count())
    results   = collection.query(query_texts=[query], n_results=n)
    chunks    = results["documents"][0]
    distances = results["distances"][0]
    return chunks, distances


# ─── CONFIDENCE SCORING ─────────────────────────────────────
def score_confidence(distances: list) -> tuple:
    """
    Convert retrieval distances to a confidence tier.

    PM Decision: Three-tier system (HIGH / MEDIUM / LOW)
    mirrors the HITL gate design used in DemandSense —
    consistent product language across the portfolio.
    """
    best = min(distances) if distances else 1.0
    sim  = round(1 - best, 3)

    if best < CONF_HIGH:
        return "HIGH", sim
    elif best < CONF_MED:
        return "MEDIUM", sim
    else:
        return "LOW", sim


# ─── SYSTEM PROMPT ──────────────────────────────────────────
SYSTEM_PROMPT = """You are FinDoc Intelligence — an expert
financial document analyst.

RULES (non-negotiable):
1. Answer using ONLY the document context provided.
2. If context is insufficient, respond with exactly:
   "I cannot find sufficient information in this document."
3. Always cite which section supports your answer.
4. For numbers, dates, percentages — be precise, never approximate.
5. Never guess or use outside knowledge.

FORMAT every response as:
ANSWER: [your direct answer]
SOURCE: [exact quote or section reference from the document]
"""


# ─── ANSWER GENERATION ──────────────────────────────────────
def generate_answer(query: str, chunks: list,
                    distances: list) -> dict:
    """
    Generate a grounded answer using Groq + retrieved context.

    PM Decision: Structured ANSWER + SOURCE output format.
    Forces citation on every response — reduces hallucination
    risk vs free-form generation without increasing latency.

    PM Decision: temperature = 0.1 (not 0.0)
    Pure 0.0 causes repetitive phrasing on long answers.
    0.1 adds minimal variation while keeping factual accuracy.

    PM Decision: Low confidence → skip LLM call entirely.
    Saves ~$0.002/query at scale and avoids hallucination
    on queries the document cannot answer.
    """
    confidence, similarity = score_confidence(distances)

    # Fallback gate — do not call LLM if confidence is LOW
    if confidence == "LOW":
        return {
            "answer"     : "I cannot find sufficient information "
                           "in this document to answer that question.",
            "source"     : "No relevant section found.",
            "confidence" : "LOW",
            "similarity" : similarity,
            "chunks_used": 0,
            "tokens_used": 0
        }

    context = "\n\n---\n\n".join(
        f"[Section {i+1}]\n{c}" for i, c in enumerate(chunks)
    )

    user_msg = f"""Context from the financial document:
{context}

Question: {query}

Answer based only on the context above."""

    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    except Exception:
        api_key = os.getenv("GROQ_API_KEY")

    client  = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model    = MODEL,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg}
        ],
        temperature = 0.1,
        max_tokens  = 512
    )

    raw    = response.choices[0].message.content.strip()
    answer = raw
    source = "See document context."

    if "SOURCE:" in raw:
        parts  = raw.split("SOURCE:", 1)
        answer = parts[0].replace("ANSWER:", "").strip()
        source = parts[1].strip()
    elif "ANSWER:" in raw:
        answer = raw.replace("ANSWER:", "").strip()

    return {
        "answer"     : answer,
        "source"     : source,
        "confidence" : confidence,
        "similarity" : similarity,
        "chunks_used": len(chunks),
        "tokens_used": response.usage.total_tokens
    }


# ─── MAIN PIPELINE ──────────────────────────────────────────
def run_pipeline(file_path: str, query: str,
                 doc_name: str = "document") -> dict:
    """
    End-to-end RAG: file path + query → grounded answer.
    This is the single function the Streamlit app calls.
    """
    text       = load_document(file_path)
    chunks     = chunk_text(text)
    collection = build_vector_store(chunks, doc_name)
    ctx_chunks, distances = retrieve_context(query, collection)
    result     = generate_answer(query, ctx_chunks, distances)

    result["total_chunks"] = len(chunks)
    result["doc_name"]     = doc_name
    return result