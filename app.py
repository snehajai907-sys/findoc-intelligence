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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #080C14;
}
.block-container {
    padding: 2rem 3rem;
    max-width: 1080px;
    background: #080C14;
}
.main { background: #080C14; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0A0E1A !important;
    border-right: 1px solid #1A2438;
}
[data-testid="stSidebar"] * { color: #8899AA !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #131D2E !important;
    border: 1px solid #1E2D4A !important;
    color: #94A3B8 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    padding: 6px 12px !important;
    box-shadow: none !important;
}

/* ── UPLOAD ZONE ── */
[data-testid="stFileUploader"] {
    background: #0D1421;
    border: 1.5px dashed #1E3A5F;
    border-radius: 16px;
    padding: 8px;
    transition: all 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #3B82F6;
    background: #0F1E35;
}
[data-testid="stFileUploader"] * { color: #64748B !important; }
[data-testid="stFileUploader"] button {
    background: #1E3A5F !important;
    color: #93C5FD !important;
    border: none !important;
    border-radius: 8px !important;
}

/* ── INPUTS ── */
.stTextInput input {
    background: #0D1421 !important;
    border: 1.5px solid #1E2D4A !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 14px 18px !important;
    caret-color: #3B82F6;
}
.stTextInput input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
.stTextInput input::placeholder { color: #2D3D52 !important; }
.stTextInput label { color: #4A5568 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 20px !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(37,99,235,0.45) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #0D1421 !important;
    border: 1px solid #1E2D4A !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: #64748B !important; }
[data-testid="stExpander"] p,
[data-testid="stExpander"] td,
[data-testid="stExpander"] th { color: #64748B !important; }

/* ── SPINNER ── */
[data-testid="stSpinner"] * { color: #3B82F6 !important; }

/* ── SUCCESS/ERROR ── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── CARDS ── */
.hero-banner {
    background: linear-gradient(135deg, #0D1B35 0%, #0A1628 50%, #06101E 100%);
    border: 1px solid #1E3A5F;
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #F1F5F9;
    margin: 0;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.hero-title span { color: #3B82F6; }
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #4A6080;
    margin-top: 10px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #60A5FA;
    letter-spacing: 0.04em;
    margin-bottom: 16px;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    color: #2D4A6A;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.answer-card {
    background: linear-gradient(145deg, #0D1827, #0A1220);
    border: 1px solid #1E3050;
    border-radius: 16px;
    padding: 28px;
    margin-top: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 
                inset 0 1px 0 rgba(255,255,255,0.03);
}
.conf-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 20px;
}
.badge-high {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.25);
    color: #34D399;
}
.badge-med {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.25);
    color: #FBBF24;
}
.badge-low {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    color: #F87171;
}
.answer-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    color: #2D4A6A;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.answer-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: #CBD5E1;
    line-height: 1.75;
    font-weight: 400;
}
.source-card {
    background: rgba(14,165,233,0.05);
    border: 1px solid rgba(14,165,233,0.15);
    border-left: 3px solid #0EA5E9;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 20px;
}
.source-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    color: #0EA5E9;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
}
.source-text {
    font-size: 0.85rem;
    color: #7DD3FC;
    line-height: 1.6;
    font-style: italic;
}
.meta-row {
    display: flex;
    gap: 0;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #111D2E;
    flex-wrap: wrap;
}
.meta-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0 16px;
    border-right: 1px solid #111D2E;
    min-width: 80px;
}
.meta-item:first-child { padding-left: 0; }
.meta-item:last-child { border-right: none; }
.meta-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #2D4A6A;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.meta-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #60A5FA;
    font-weight: 500;
}
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #0D1827;
    border: 1px solid #1E3050;
    border-radius: 8px;
    padding: 5px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #4A7FA5;
    margin: 3px;
}
.stat-chip strong { color: #60A5FA; font-weight: 600; }
.step-grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 12px;
    margin-top: 20px;
}
.step-card {
    background: #0D1421;
    border: 1px solid #1A2438;
    border-radius: 12px;
    padding: 18px;
    transition: border-color 0.2s;
}
.step-card:hover { border-color: #3B82F6; }
.step-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #1E3A5F;
    line-height: 1;
    margin-bottom: 10px;
}
.step-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #CBD5E1;
    margin-bottom: 4px;
}
.step-desc { font-size: 0.75rem; color: #334155; line-height: 1.4; }
.history-item {
    background: #0A0F1A;
    border: 1px solid #131D2E;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.history-item:hover { border-color: #1E3050; }
.history-q {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94A3B8;
}
.history-a { font-size: 0.78rem; color: #334155; margin-top: 5px; }
.upload-hero {
    background: linear-gradient(135deg, #0A1628 0%, #080C14 100%);
    border: 1.5px dashed #1E3A5F;
    border-radius: 20px;
    padding: 48px 32px;
    text-align: center;
    margin-bottom: 28px;
    transition: all 0.3s;
}
.upload-hero:hover {
    border-color: #3B82F6;
    background: linear-gradient(135deg, #0D1E38 0%, #0A1020 100%);
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────
for key, val in [("history",[]),("collection",None),
                 ("doc_stats",{}),("total_tokens",0),
                 ("query_input","")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 24px 0;'>
        <div style='font-family:"Syne",sans-serif;font-size:1rem;
                    font-weight:700;color:#60A5FA;letter-spacing:0.02em;'>
            FinDoc
        </div>
        <div style='font-size:0.7rem;color:#1E3050;margin-top:2px;
                    font-family:"JetBrains Mono",monospace;'>
            INTELLIGENCE v2.0
        </div>
    </div>
    <div style='font-family:"JetBrains Mono",monospace;font-size:0.65rem;
                color:#1E3050;letter-spacing:0.1em;margin-bottom:10px;'>
        DOCUMENT
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload", type=["pdf","txt"],
        label_visibility="collapsed"
    )

    if uploaded:
        with st.spinner("Processing..."):
            suffix = ".pdf" if uploaded.name.endswith(".pdf") else ".txt"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.read()); tmp.flush(); tmp.close()
            from rag_pipeline import load_document, chunk_text, build_vector_store
            text   = load_document(tmp.name)
            chunks = chunk_text(text)
            col    = build_vector_store(chunks, uploaded.name)
            st.session_state.collection   = col
            st.session_state.doc_stats    = {
                "name":uploaded.name,
                "words":len(text.split()),
                "chunks":len(chunks)
            }
            st.session_state.history      = []
            st.session_state.total_tokens = 0
        st.success("Document indexed ✓")

    if st.session_state.doc_stats:
        ds = st.session_state.doc_stats
        name = ds['name'][:24] + "..." if len(ds['name']) > 24 else ds['name']
        st.markdown(f"""
        <div style='margin-top:20px;padding:16px;background:#0D1421;
                    border:1px solid #1A2438;border-radius:12px;'>
            <div style='font-size:0.75rem;color:#60A5FA;font-weight:600;
                        margin-bottom:12px;'>📄 {name}</div>
            <div>
                <span class='stat-chip'><strong>{ds['words']:,}</strong> words</span>
                <span class='stat-chip'><strong>{ds['chunks']}</strong> chunks</span>
                <span class='stat-chip'>
                    <strong>{st.session_state.total_tokens:,}</strong> tokens used
                </span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>",
                unsafe_allow_html=True)

    with st.expander("⚙️ Config"):
        st.markdown("""
model   : llama-3.3-70b
    chunks  : 400 words
    overlap : 40 words
    top-k   : 3
    embed   : MiniLM-L6-v2
                    """)

    with st.expander("🚦 Confidence"):
        st.markdown("""
        🟢 **HIGH** · Strong match

        🟡 **MEDIUM** · Related content

        🔴 **LOW** · No context · LLM skipped
        """)

    st.markdown("""
    <div style='position:fixed;bottom:16px;left:0;width:250px;
                padding:0 16px;font-size:0.65rem;color:#1E3050;
                font-family:"JetBrains Mono",monospace;'>
        Built by Sneha Jaiswal · AI PM
    </div>""", unsafe_allow_html=True)

# ── HERO BANNER ─────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div class='hero-badge'>⚡ RAG-POWERED · LLM EVALUATED</div>
    <div class='hero-title'>
        FinDoc <span>Intelligence</span>
    </div>
    <div class='hero-sub'>
        Upload any financial document · Get grounded, cited answers
        with confidence scoring · Zero hallucinations guaranteed
    </div>
</div>
""", unsafe_allow_html=True)

# ── NO DOC STATE ─────────────────────────────────────────────
if not st.session_state.collection:
    st.markdown("""
    <div class='upload-hero'>
        <div style='font-size:3rem;margin-bottom:16px;'>📂</div>
        <div style='font-family:"Syne",sans-serif;font-size:1.3rem;
                    font-weight:700;color:#CBD5E1;margin-bottom:8px;'>
            No document loaded
        </div>
        <div style='font-size:0.85rem;color:#2D4A6A;margin-bottom:24px;'>
            Upload a PDF or TXT from the sidebar to begin analysis
        </div>
        <div style='display:flex;gap:10px;justify-content:center;flex-wrap:wrap;'>
            <span style='background:#0D1827;border:1px solid #1E3050;
                         padding:6px 14px;border-radius:8px;
                         font-size:0.75rem;color:#3B82F6;
                         font-family:"JetBrains Mono",monospace;'>
                Annual Reports
            </span>
            <span style='background:#0D1827;border:1px solid #1E3050;
                         padding:6px 14px;border-radius:8px;
                         font-size:0.75rem;color:#3B82F6;
                         font-family:"JetBrains Mono",monospace;'>
                Earnings Releases
            </span>
            <span style='background:#0D1827;border:1px solid #1E3050;
                         padding:6px 14px;border-radius:8px;
                         font-size:0.75rem;color:#3B82F6;
                         font-family:"JetBrains Mono",monospace;'>
                Loan Agreements
            </span>
            <span style='background:#0D1827;border:1px solid #1E3050;
                         padding:6px 14px;border-radius:8px;
                         font-size:0.75rem;color:#3B82F6;
                         font-family:"JetBrains Mono",monospace;'>
                SEC Filings
            </span>
        </div>
    </div>
    <div class='step-grid'>
        <div class='step-card'>
            <div class='step-num'>01</div>
            <div class='step-title'>Upload</div>
            <div class='step-desc'>PDF or TXT · Any financial document</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>02</div>
            <div class='step-title'>Index</div>
            <div class='step-desc'>Auto-chunked and embedded instantly</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>03</div>
            <div class='step-title'>Ask</div>
            <div class='step-desc'>Revenue, margins, debt, risks</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>04</div>
            <div class='step-title'>Answer</div>
            <div class='step-desc'>Cited, grounded, confidence-scored</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Q&A INTERFACE ────────────────────────────────────────────
st.markdown("<div class='section-label'>SUGGESTED QUERIES</div>",
            unsafe_allow_html=True)

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

st.markdown("<div style='margin-top:12px;'></div>",
            unsafe_allow_html=True)

query = st.text_input(
    "q", key="query_input",
    placeholder="Ask anything about this document...",
    label_visibility="collapsed"
)

btn_col, _ = st.columns([2, 8])
with btn_col:
    ask = st.button("⚡  Analyze", type="primary",
                    use_container_width=True)

# ── PROCESS ─────────────────────────────────────────────────
if ask and query.strip():
    with st.spinner("Scanning document..."):
        start = time.time()
        from rag_pipeline import retrieve_context, generate_answer
        chunks, distances = retrieve_context(
            query, st.session_state.collection
        )
        result  = generate_answer(query, chunks, distances)
        elapsed = round(time.time() - start, 2)
    st.session_state.total_tokens += result.get("tokens_used", 0)
    st.session_state.history.append({
        "query":query, "result":result, "elapsed":elapsed
    })

# ── DISPLAY ANSWER ───────────────────────────────────────────
i# ── DISPLAY ANSWER ───────────────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[-1]
    r      = latest["result"]
    conf   = r["confidence"]

    badge_map = {
        "HIGH":   ("badge-high","● HIGH CONFIDENCE",
                   "Strong semantic match · Answer is reliable"),
        "MEDIUM": ("badge-med","● MEDIUM CONFIDENCE",
                   "Related context found · Verify numerical data"),
        "LOW":    ("badge-low","● LOW CONFIDENCE — FALLBACK",
                   "Insufficient context · LLM call skipped · No hallucination risk"),
    }
    badge_css, badge_label, badge_desc = badge_map[conf]
    sim_clean = round(r["similarity"], 3)
    ans = r["answer"].replace("<","&lt;").replace(">","&gt;")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Card wrapper open
    st.markdown("<div class='answer-card'>", unsafe_allow_html=True)

    # Badge + desc
    st.markdown(
        f"<span class='conf-badge {badge_css}'>{badge_label}</span>"
        f"<div style='font-size:0.75rem;color:#2D4A6A;"
        f"margin-bottom:20px;'>{badge_desc}</div>",
        unsafe_allow_html=True
    )

    # Answer
    st.markdown(
        f"<div class='answer-label'>Response</div>"
        f"<div class='answer-text'>{ans}</div>",
        unsafe_allow_html=True
    )

    # Source
    if r["source"] not in ["No relevant section found.",
                            "See document context."]:
        src = r["source"].replace("<","&lt;").replace(">","&gt;")
        st.markdown(
            f"<div class='source-card'>"
            f"<div class='source-label'>📎 SOURCE CITATION</div>"
            f"<div class='source-text'>{src}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Divider
    st.markdown(
        "<div style='border-top:1px solid #111D2E;"
        "margin-top:20px;padding-top:16px;'></div>",
        unsafe_allow_html=True
    )

    # Meta row using Streamlit columns (most reliable)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Confidence",  conf)
    m2.metric("Similarity",  str(sim_clean))
    m3.metric("Chunks",      str(r["chunks_used"]))
    m4.metric("Tokens",      str(r["tokens_used"]))
    m5.metric("Latency",     f"{latest['elapsed']}s")

    # Card wrapper close
    st.markdown("</div>", unsafe_allow_html=True)
    
# ── HISTORY ──────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("""
    <div style='margin-top:32px;'>
    <div class='section-label'>QUERY HISTORY</div>
    </div>""", unsafe_allow_html=True)

    icons = {"HIGH":"🟢","MEDIUM":"🟡","LOW":"🔴"}
    for item in reversed(st.session_state.history[:-1]):
        r   = item["result"]
        ans = r["answer"][:120].replace(
            "<","&lt;").replace(">","&gt;")
        st.markdown(f"""
        <div class='history-item'>
            <div class='history-q'>
                {icons[r['confidence']]} &nbsp; {item['query']}
            </div>
            <div class='history-a'>{ans}...</div>
        </div>""", unsafe_allow_html=True)