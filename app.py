# ============================================================
# FINDOC INTELLIGENCE — File 2: Streamlit App
# PM Purpose: This IS the product. A credit analyst uploads
# a financial document and gets grounded, cited answers
# with explicit confidence indicators.
# ============================================================

import streamlit as st
import tempfile
import os
import time
from dotenv import load_dotenv
load_dotenv()

from rag_pipeline import run_pipeline, load_document, chunk_text

# ─── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="FinDoc Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── STYLING ────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }

    .conf-high {
        background: #F0FDF4; border-left: 4px solid #16A34A;
        padding: 12px 16px; border-radius: 6px; margin: 8px 0;
    }
    .conf-med {
        background: #FFFBEB; border-left: 4px solid #D97706;
        padding: 12px 16px; border-radius: 6px; margin: 8px 0;
    }
    .conf-low {
        background: #FEF2F2; border-left: 4px solid #DC2626;
        padding: 12px 16px; border-radius: 6px; margin: 8px 0;
    }
    .answer-box {
        background: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 16px; border-radius: 8px; margin: 8px 0;
        font-size: 1rem; line-height: 1.6;
    }
    .source-box {
        background: #EFF6FF; border: 1px solid #BFDBFE;
        padding: 12px; border-radius: 6px; margin: 8px 0;
        font-size: 0.88rem; color: #1E40AF;
    }
    .metric-card {
        background: white; border: 1px solid #E2E8F0;
        padding: 12px; border-radius: 8px; text-align: center;
    }
    .section-label {
        font-size: 0.75rem; font-weight: 600; color: #64748B;
        letter-spacing: 0.08em; margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ───────────────────────────────────────────
if "history"    not in st.session_state:
    st.session_state.history     = []
if "collection" not in st.session_state:
    st.session_state.collection  = None
if "doc_name"   not in st.session_state:
    st.session_state.doc_name    = None
if "doc_stats"  not in st.session_state:
    st.session_state.doc_stats   = {}
if "tmp_path"   not in st.session_state:
    st.session_state.tmp_path    = None
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# ─── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📄 FinDoc Intelligence")
    st.markdown("*AI-powered financial document Q&A*")
    st.markdown("---")

    uploaded = st.file_uploader(
        "Upload Financial Document",
        type=["pdf", "txt"],
        help="Supports PDF and TXT formats"
    )

    if uploaded:
        with st.spinner("Processing document..."):
            # Save to temp file
            suffix = ".pdf" if uploaded.name.endswith(".pdf") else ".txt"
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix=suffix
            )
            tmp.write(uploaded.read())
            tmp.flush()
            tmp_path = tmp.name
            tmp.close()

            # Process
            from rag_pipeline import (
                load_document, chunk_text, build_vector_store
            )
            text   = load_document(tmp_path)
            chunks = chunk_text(text)
            col    = build_vector_store(chunks, uploaded.name)

            # Store in session
            st.session_state.collection = col
            st.session_state.doc_name   = uploaded.name
            st.session_state.tmp_path   = tmp_path
            st.session_state.doc_stats  = {
                "words"  : len(text.split()),
                "chunks" : len(chunks),
                "name"   : uploaded.name
            }
            st.session_state.history      = []
            st.session_state.total_tokens = 0

        st.success(f"✅ Document ready")

    # Document stats
    if st.session_state.doc_stats:
        ds = st.session_state.doc_stats
        st.markdown("---")
        st.markdown("**Document Stats**")
        st.markdown(f"📄 `{ds['name']}`")
        st.markdown(f"📝 {ds['words']:,} words")
        st.markdown(f"🧩 {ds['chunks']} chunks indexed")
        st.markdown(f"🔢 {st.session_state.total_tokens:,} tokens used")

    st.markdown("---")

    # PM Decision explanations
    with st.expander("⚙️ System Configuration"):
        st.markdown("""
        **Chunking:** 400 words / 40 overlap
        **Retrieval:** Top-3 chunks per query
        **Model:** Llama 3.3 70B via Groq
        **Embeddings:** all-MiniLM-L6-v2
        **Confidence CI:** Cosine distance threshold
        """)

    with st.expander("🚦 Confidence Guide"):
        st.markdown("""
        🟢 **HIGH** — Strong match found. Answer reliable.

        🟡 **MEDIUM** — Related content found. Verify key
        numbers independently.

        🔴 **LOW** — Insufficient context. LLM call skipped
        to prevent hallucination.
        """)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#94A3B8;'>
    FinDoc Intelligence v1.0<br>
    Built by Sneha Jaiswal · AI PM Portfolio
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN PANEL ─────────────────────────────────────────────
col_title, col_status = st.columns([4, 1])
with col_title:
    st.markdown("# 📄 FinDoc Intelligence")
    st.markdown(
        "**Upload a financial document. Ask anything. "
        "Get grounded, cited answers with confidence scores.**"
    )
with col_status:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.collection:
        st.success("Document Loaded ✅")
    else:
        st.warning("No Document ⚠️")

st.markdown("---")

# ─── NO DOCUMENT STATE ──────────────────────────────────────
if not st.session_state.collection:
    st.info(
        "👈 Upload a financial document in the sidebar to begin. "
        "Supports PDF and TXT files."
    )

    st.markdown("### 💡 Example Use Cases")
    cols = st.columns(3)
    examples = [
        ("🏦 Credit Analysis",
         "What is the debt-to-equity ratio and how has it trended?"),
        ("📊 Earnings Review",
         "What were the key revenue drivers this quarter?"),
        ("⚖️ Risk Assessment",
         "What risks did management highlight in the outlook?"),
    ]
    for c, (title, q) in zip(cols, examples):
        with c:
            st.markdown(f"**{title}**")
            st.markdown(f"*\"{q}\"*")

    st.markdown("---")
    st.markdown("### 🏗️ How It Works")
    steps = st.columns(4)
    for col, (num, step) in zip(steps, [
        ("1", "Upload financial document"),
        ("2", "System chunks + indexes it"),
        ("3", "Ask your question"),
        ("4", "Get grounded answer + citation"),
    ]):
        with col:
            st.markdown(f"**Step {num}**")
            st.markdown(step)
    st.stop()


# ─── Q&A INTERFACE ──────────────────────────────────────────
st.markdown("### 💬 Ask Your Question")

# Suggested questions
st.markdown(
    '<p class="section-label">SUGGESTED QUESTIONS</p>',
    unsafe_allow_html=True
)
suggestions = [
    "What was the total revenue?",
    "What is the net income margin?",
    "What is the debt position?",
    "What is the management outlook?",
]
s_cols = st.columns(len(suggestions))
for col, sug in zip(s_cols, suggestions):
    if col.button(sug, use_container_width=True):
        st.session_state["query_input"] = sug

query = st.text_input(
    "Your question",
    key="query_input",
    placeholder="e.g. What was the revenue growth rate?",
    label_visibility="collapsed"
)

ask_btn = st.button("🔍 Get Answer", type="primary",
                    use_container_width=False)

# ─── PROCESS QUERY ──────────────────────────────────────────
if ask_btn and query.strip():
    with st.spinner("Searching document and generating answer..."):
        start = time.time()

        from rag_pipeline import (
            retrieve_context, generate_answer, score_confidence
        )
        chunks, distances = retrieve_context(
            query, st.session_state.collection
        )
        result = generate_answer(query, chunks, distances)
        elapsed = round(time.time() - start, 2)

    # Update token counter
    st.session_state.total_tokens += result.get("tokens_used", 0)

    # Add to history
    st.session_state.history.append({
        "query"   : query,
        "result"  : result,
        "elapsed" : elapsed
    })

# ─── DISPLAY LATEST ANSWER ──────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[-1]
    r      = latest["result"]
    conf   = r["confidence"]

    st.markdown("---")
    st.markdown("### 🎯 Answer")

    # Confidence banner
    conf_labels = {
        "HIGH"  : ("🟢", "HIGH CONFIDENCE",
                   "conf-high",
                   "Strong match found — answer is reliable."),
        "MEDIUM": ("🟡", "MEDIUM CONFIDENCE",
                   "conf-med",
                   "Related content found — verify key numbers independently."),
        "LOW"   : ("🔴", "LOW CONFIDENCE — FALLBACK TRIGGERED",
                   "conf-low",
                   "Insufficient context in document. LLM call skipped to prevent hallucination."),
    }
    icon, label, css, desc = conf_labels[conf]
    st.markdown(
        f'<div class="{css}"><b>{icon} {label}</b><br>'
        f'<span style="font-size:0.85rem">{desc}</span>'
        f'<span style="float:right; font-size:0.8rem; color:#64748B;">'
        f'Similarity: {r["similarity"]} | '
        f'Chunks used: {r["chunks_used"]} | '
        f'Tokens: {r["tokens_used"]} | '
        f'Time: {latest["elapsed"]}s</span></div>',
        unsafe_allow_html=True
    )

    # Answer
    st.markdown(
        f'<div class="answer-box">{r["answer"]}</div>',
        unsafe_allow_html=True
    )

    # Source
    if r["source"] and r["source"] != "No relevant section found.":
        st.markdown(
            '<p class="section-label">📎 SOURCE CITATION</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="source-box">{r["source"]}</div>',
            unsafe_allow_html=True
        )

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Confidence",   conf)
    m2.metric("Similarity",   r["similarity"])
    m3.metric("Tokens Used",  r["tokens_used"])
    m4.metric("Response Time", f"{latest['elapsed']}s")


# ─── CONVERSATION HISTORY ───────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.markdown("### 📜 Conversation History")

    for i, item in enumerate(
        reversed(st.session_state.history[:-1]), 1
    ):
        r = item["result"]
        conf_colors = {
            "HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"
        }
        with st.expander(
            f"{conf_colors[r['confidence']]}  Q: {item['query'][:80]}..."
        ):
            st.markdown(f"**Answer:** {r['answer']}")
            st.markdown(f"**Confidence:** {r['confidence']} "
                        f"({r['similarity']})")
            st.markdown(f"**Tokens:** {r['tokens_used']}")