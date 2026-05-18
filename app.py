# ============================================================
# FINDOC INTELLIGENCE — Redesigned UI v2
# ============================================================

import streamlit as st
import tempfile, os, time
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="FinDoc Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1100px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0F172A;
    border-right: 1px solid #1E293B;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong { color: #F1F5F9 !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #94A3B8 !important; }

/* ── HEADER ── */
.app-header {
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 4px;
}
.app-icon {
    width: 44px; height: 44px; background: #2563EB;
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 22px;
    box-shadow: 0 4px 12px rgba(37,99,235,0.3);
}
.app-title { font-size: 1.75rem; font-weight: 700; color: #0F172A; }
.app-subtitle { font-size: 0.88rem; color: #64748B; margin-bottom: 1.5rem; }

/* ── UPLOAD ZONE ── */
.upload-zone {
    border: 2px dashed #CBD5E1; border-radius: 12px;
    padding: 2.5rem; text-align: center;
    background: #F8FAFC; margin-bottom: 1.5rem;
    transition: all 0.2s;
}
.upload-zone:hover { border-color: #2563EB; background: #EFF6FF; }

/* ── SUGGESTION PILLS ── */
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }
.pill {
    background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE;
    padding: 6px 14px; border-radius: 20px; font-size: 0.82rem;
    font-weight: 500; cursor: pointer; transition: all 0.2s;
}
.pill:hover { background: #2563EB; color: white; }

/* ── INPUT ── */
.stTextInput input {
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    background: #FAFAFA !important;
    transition: all 0.2s !important;
}
.stTextInput input:focus {
    border-color: #2563EB !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
}

/* ── ANSWER CARD ── */
.answer-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}
.conf-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 14px; border-radius: 20px;
    font-size: 0.78rem; font-weight: 600;
    letter-spacing: 0.04em; margin-bottom: 16px;
}
.badge-high { background:#DCFCE7; color:#15803D; border:1px solid #86EFAC; }
.badge-med  { background:#FEF9C3; color:#A16207; border:1px solid #FDE047; }
.badge-low  { background:#FEE2E2; color:#B91C1C; border:1px solid #FCA5A5; }

.answer-label {
    font-size: 0.72rem; font-weight: 600; color: #94A3B8;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 8px;
}
.answer-text {
    font-size: 1.02rem; color: #1E293B; line-height: 1.7;
    font-weight: 400;
}
.source-card {
    background: #F0F9FF; border: 1px solid #BAE6FD;
    border-left: 3px solid #0EA5E9;
    border-radius: 8px; padding: 12px 16px;
    margin-top: 16px;
}
.source-label {
    font-size: 0.7rem; font-weight: 600; color: #0369A1;
    letter-spacing: 0.06em; margin-bottom: 4px;
}
.source-text { font-size: 0.88rem; color: #0C4A6E; line-height: 1.5; }

/* ── META ROW ── */
.meta-row {
    display: flex; gap: 20px; margin-top: 16px;
    padding-top: 14px; border-top: 1px solid #F1F5F9;
    flex-wrap: wrap;
}
.meta-item { display: flex; flex-direction: column; }
.meta-label { font-size: 0.68rem; color: #94A3B8; font-weight: 500; }
.meta-value { font-size: 0.88rem; color: #475569; font-weight: 600; }

/* ── HISTORY ── */
.history-item {
    border: 1px solid #F1F5F9; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 10px;
    background: #FAFAFA;
}
.history-q { font-size: 0.88rem; font-weight: 600; color: #1E293B; }
.history-a { font-size: 0.83rem; color: #64748B; margin-top: 4px; }

/* ── STAT PILLS ── */
.stat-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
.stat-pill {
    background: #1E293B; color: #94A3B8;
    padding: 5px 12px; border-radius: 8px;
    font-size: 0.75rem; font-weight: 500;
}
.stat-pill span { color: #F1F5F9; font-weight: 700; }

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center; padding: 3rem 2rem;
    border: 1.5px dashed #E2E8F0; border-radius: 16px;
    margin-top: 2rem; background: #FAFAFA;
}
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-title { font-size: 1.1rem; font-weight: 600;
               color: #1E293B; margin-bottom: 6px; }
.empty-sub { font-size: 0.88rem; color: #94A3B8; }

/* ── HOW IT WORKS ── */
.step-row { display: flex; gap: 12px; margin-top: 1.5rem; }
.step-card {
    flex: 1; background: white; border: 1px solid #E2E8F0;
    border-radius: 12px; padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.step-num {
    width: 28px; height: 28px; background: #2563EB;
    border-radius: 8px; color: white; font-size: 0.8rem;
    font-weight: 700; display: flex; align-items: center;
    justify-content: center; margin-bottom: 10px;
}
.step-title { font-size: 0.88rem; font-weight: 600; color: #1E293B; }
.step-desc { font-size: 0.78rem; color: #94A3B8; margin-top: 4px; }

/* ── BUTTON ── */
.stButton > button {
    background: #2563EB !important; color: white !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 24px !important; font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #1D4ED8 !important;
    box-shadow: 0 6px 16px rgba(37,99,235,0.4) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stFileUploader"] {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────
for key, default in [
    ("history", []),
    ("collection", None),
    ("doc_stats", {}),
    ("total_tokens", 0),
    ("query_input", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 20px 0;'>
        <div style='font-size:1.1rem; font-weight:700;
                    color:#F1F5F9; margin-bottom:4px;'>
            📄 FinDoc Intelligence
        </div>
        <div style='font-size:0.78rem; color:#64748B;'>
            AI-powered financial document Q&A
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload Document",
        type=["pdf", "txt"],
        label_visibility="collapsed",
        help="Upload any financial PDF or TXT document"
    )

    if uploaded:
        with st.spinner("Indexing document..."):
            suffix = ".pdf" if uploaded.name.endswith(".pdf") else ".txt"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.read())
            tmp.flush(); tmp.close()

            from rag_pipeline import load_document, chunk_text, build_vector_store
            text   = load_document(tmp.name)
            chunks = chunk_text(text)
            col    = build_vector_store(chunks, uploaded.name)

            st.session_state.collection   = col
            st.session_state.doc_stats    = {
                "name": uploaded.name,
                "words": len(text.split()),
                "chunks": len(chunks)
            }
            st.session_state.history      = []
            st.session_state.total_tokens = 0

        st.success("Ready to answer questions")

    # Doc stats
    if st.session_state.doc_stats:
        ds = st.session_state.doc_stats
        st.markdown(f"""
        <div style='margin-top:16px;'>
            <div style='font-size:0.7rem; color:#475569;
                        font-weight:600; letter-spacing:0.06em;
                        margin-bottom:10px;'>DOCUMENT LOADED</div>
            <div style='font-size:0.82rem; color:#CBD5E1;
                        margin-bottom:12px; word-break:break-all;'>
                📄 {ds['name']}
            </div>
            <div class='stat-row'>
                <div class='stat-pill'><span>{ds['words']:,}</span> words</div>
                <div class='stat-pill'><span>{ds['chunks']}</span> chunks</div>
                <div class='stat-pill'><span>{st.session_state.total_tokens:,}</span> tokens</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:24px;'>", unsafe_allow_html=True)
    with st.expander("⚙️ System Config"):
        st.markdown("""
        | Setting | Value |
        |---|---|
        | Model | Llama 3.3 70B |
        | Chunk size | 400 words |
        | Overlap | 40 words |
        | Retrieval | Top-3 chunks |
        | Embeddings | all-MiniLM-L6-v2 |
        | Confidence | Cosine distance |
        """)

    with st.expander("🚦 Confidence Tiers"):
        st.markdown("""
        🟢 **HIGH** — Strong match. Answer reliable.

        🟡 **MEDIUM** — Related content found.
        Verify key numbers independently.

        🔴 **LOW** — No sufficient context found.
        LLM call skipped. Zero hallucination risk.
        """)

    st.markdown(f"""
    <div style='position:fixed; bottom:20px; left:0; width:260px;
                padding:0 16px; font-size:0.7rem; color:#334155;'>
        FinDoc Intelligence v2.0 · Built by Sneha Jaiswal
    </div>
    """, unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────
st.markdown("""
<div class='app-header'>
    <div class='app-icon'>📄</div>
    <div class='app-title'>FinDoc Intelligence</div>
</div>
<div class='app-subtitle'>
    Upload any financial document · Ask anything ·
    Get grounded, cited answers with confidence scores
</div>
""", unsafe_allow_html=True)

# ── NO DOCUMENT STATE ────────────────────────────────────────
if not st.session_state.collection:
    st.markdown("""
    <div class='empty-state'>
        <div class='empty-icon'>📂</div>
        <div class='empty-title'>No document loaded yet</div>
        <div class='empty-sub'>
            Upload a PDF or TXT file from the sidebar to begin
        </div>
    </div>

    <div class='step-row' style='margin-top:24px;'>
        <div class='step-card'>
            <div class='step-num'>1</div>
            <div class='step-title'>Upload Document</div>
            <div class='step-desc'>PDF or TXT · Any financial document</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>2</div>
            <div class='step-title'>Auto-Indexed</div>
            <div class='step-desc'>Chunked, embedded and ready instantly</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>3</div>
            <div class='step-title'>Ask Anything</div>
            <div class='step-desc'>Revenue, margins, debt, outlook</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>4</div>
            <div class='step-title'>Grounded Answer</div>
            <div class='step-desc'>Cited, confidence-scored, no hallucinations</div>
        </div>
    </div>

    <div style='margin-top:28px;'>
        <div style='font-size:0.75rem; font-weight:600; color:#94A3B8;
                    letter-spacing:0.06em; margin-bottom:12px;'>
            EXAMPLE QUESTIONS
        </div>
        <div class='pill-row'>
            <span class='pill'>What was the total revenue?</span>
            <span class='pill'>What is the net income margin?</span>
            <span class='pill'>What is the debt position?</span>
            <span class='pill'>What risks did management highlight?</span>
            <span class='pill'>What is the revenue growth rate?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Q&A INTERFACE ────────────────────────────────────────────
st.markdown("""
<div style='font-size:0.72rem; font-weight:600; color:#94A3B8;
            letter-spacing:0.08em; margin-bottom:8px;'>
    SUGGESTED QUESTIONS
</div>
""", unsafe_allow_html=True)

suggestions = [
    "What was the total revenue?",
    "What is the net income margin?",
    "What is the debt position?",
    "What is the management outlook?",
]
cols = st.columns(len(suggestions))
for col, sug in zip(cols, suggestions):
    if col.button(sug, use_container_width=True):
        st.session_state["query_input"] = sug

query = st.text_input(
    "question",
    key="query_input",
    placeholder="Ask anything about this document...",
    label_visibility="collapsed"
)

btn_col, _ = st.columns([2, 8])
with btn_col:
    ask = st.button("🔍  Get Answer", type="primary",
                    use_container_width=True)

# ── PROCESS ─────────────────────────────────────────────────
if ask and query.strip():
    with st.spinner("Searching document..."):
        start = time.time()
        from rag_pipeline import retrieve_context, generate_answer
        chunks, distances = retrieve_context(
            query, st.session_state.collection
        )
        result  = generate_answer(query, chunks, distances)
        elapsed = round(time.time() - start, 2)

    st.session_state.total_tokens += result.get("tokens_used", 0)
    st.session_state.history.append({
        "query": query, "result": result, "elapsed": elapsed
    })

# ── LATEST ANSWER ────────────────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[-1]
    r      = latest["result"]
    conf   = r["confidence"]

    badge_map = {
        "HIGH":   ("badge-high", "🟢  HIGH CONFIDENCE",
                   "Strong match found — answer is reliable"),
        "MEDIUM": ("badge-med",  "🟡  MEDIUM CONFIDENCE",
                   "Related content found — verify key numbers independently"),
        "LOW":    ("badge-low",  "🔴  LOW CONFIDENCE — FALLBACK",
                   "Insufficient context · LLM call skipped · Zero hallucination risk"),
    }
    badge_css, badge_label, badge_desc = badge_map[conf]

    st.markdown(f"""
    <div class='answer-card'>
        <span class='conf-badge {badge_css}'>{badge_label}</span>
        <div style='font-size:0.72rem; color:#94A3B8;
                    margin-bottom:16px;'>{badge_desc}</div>

        <div class='answer-label'>Answer</div>
        <div class='answer-text'>{r['answer']}</div>

        {f"""
        <div class='source-card' style='margin-top:16px;'>
            <div class='source-label'>📎 Source Citation</div>
            <div class='source-text'>{r['source']}</div>
        </div>
        """ if r['source'] not in ['No relevant section found.',
                                    'See document context.'] else ""}

        <div class='meta-row'>
            <div class='meta-item'>
                <span class='meta-label'>Confidence</span>
                <span class='meta-value'>{conf}</span>
            </div>
            <div class='meta-item'>
                <span class='meta-label'>Similarity</span>
                <span class='meta-value'>{r['similarity']}</span>
            </div>
            <div class='meta-item'>
                <span class='meta-label'>Chunks Used</span>
                <span class='meta-value'>{r['chunks_used']}</span>
            </div>
            <div class='meta-item'>
                <span class='meta-label'>Tokens</span>
                <span class='meta-value'>{r['tokens_used']}</span>
            </div>
            <div class='meta-item'>
                <span class='meta-label'>Response Time</span>
                <span class='meta-value'>{latest['elapsed']}s</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── HISTORY ──────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("""
    <div style='font-size:0.72rem; font-weight:600; color:#94A3B8;
                letter-spacing:0.08em; margin: 28px 0 12px 0;'>
        CONVERSATION HISTORY
    </div>
    """, unsafe_allow_html=True)

    icons = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}
    for item in reversed(st.session_state.history[:-1]):
        r = item["result"]
        st.markdown(f"""
        <div class='history-item'>
            <div class='history-q'>
                {icons[r['confidence']]} {item['query']}
            </div>
            <div class='history-a'>{r['answer'][:140]}...</div>
        </div>
        """, unsafe_allow_html=True)