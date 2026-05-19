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
# ── DEMO DOCUMENT ────────────────────────────────────────────
DEMO_DOC = """
MERIDIAN CAPITAL GROUP
ANNUAL REPORT & FINANCIAL SUMMARY — FISCAL YEAR 2023

EXECUTIVE SUMMARY
Meridian Capital Group delivered a strong fiscal year 2023,
achieving record revenues of $6.84 billion, representing an
18.7% year-over-year increase from $5.76 billion in FY2022.
Net income reached $1.42 billion, up 22.4% year-over-year.
Net profit margin improved from 20.1% to 20.8%.
Earnings per share stood at $4.87 vs $3.98 in FY2022.
The Board approved a quarterly dividend of $0.68 per share,
totaling $2.72 annually — an 8% increase year-over-year.

REVENUE BY SEGMENT
Institutional Lending: $3.12 billion (45.6% of revenue), +24.3% YoY.
Retail Banking Services: $1.98 billion (28.9%), +14.1% YoY.
Wealth Management: $1.12 billion (16.4%), +11.8% YoY.
Assets under management reached $48.6 billion.
Capital Markets: $0.62 billion (9.1%), +8.4% YoY.

OPERATING EXPENSES
Total operating expenses: $4.89 billion (+16.2% vs FY2022).
Efficiency ratio improved to 71.5% from 73.1%.
Personnel costs: $2.14 billion. Technology: $0.82 billion.
R&D investment: $310 million on AI-driven credit risk tools.

BALANCE SHEET
Total assets: $94.2 billion. Total liabilities: $81.6 billion.
Shareholders equity: $12.6 billion.
Long-term debt: $18.4 billion. Short-term borrowings: $6.2 billion.
Total debt: $24.6 billion. Cash and equivalents: $8.9 billion.
Net debt position: $11.4 billion.
Debt-to-equity ratio: 1.95x (improved from 2.18x in FY2022).
CET1 capital ratio: 13.4% (above 8.0% regulatory minimum).
Return on equity: 11.8%. Return on assets: 1.51%.

CREDIT QUALITY
Non-performing loans ratio: 1.84% (improved from 2.31%).
Loan loss provisions: $420 million. Net charge-offs: $318 million.

GEOGRAPHIC PERFORMANCE
North America: $4.28 billion (62.6%). Europe: $1.37 billion (20.0%).
Asia-Pacific: $0.84 billion (12.3%), fastest growing at +41.2% YoY.
New operations in Singapore, Hong Kong, and Jakarta in Q1 2023.

RISK FACTORS
1. Interest Rate Risk: 100bps rate shift reduces NII by ~$180M annually.
2. Credit Concentration: Top 20 borrowers = 34% of total loan exposure.
3. Regulatory Risk: Basel IV could require $2.4B additional capital.
4. Geopolitical Risk: $840M in Asia-Pacific assets at regional risk.

MANAGEMENT OUTLOOK — FY2024
CEO Jonathan R. Hargrove stated the AI-driven underwriting platform
processed 68% of retail loan applications in Q4 2023 and will expand
to institutional lending in H1 2024, reducing credit decision times
from 14 days to under 72 hours.
FY2024 guidance: Revenue growth 12-15%, net margin 21.5-22.5%,
ROE target 13.0%+, capex $680-720 million.
Acquisition of Pacific Rim Financial Services valued at $2.8 billion
expected Q2 2024, adding $340M annual revenue from FY2025.

CAPITAL RETURNS
FY2023 share buybacks: $758.9 million (12.4 million shares at $61.20).
Remaining buyback authorization: $1.2 billion.
Total capital returned: $1.55 billion (109% of net income).
"""
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Outfit:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
            html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #080C14; }
.block-container { padding: 2rem 3rem; max-width: 1080px; background: #080C14; }
.main { background: #080C14; }
[data-testid="stSidebar"] { background: #0A0E1A !important; border-right: 1px solid #1A2438; }
[data-testid="stSidebar"] * { color: #8899AA !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #131D2E !important; border: 1px solid #1E2D4A !important;
    color: #94A3B8 !important; border-radius: 8px !important;
    font-size: 0.78rem !important; padding: 6px 12px !important; box-shadow: none !important;
}
[data-testid="stFileUploader"] {
    background: #0D1421; border: 1.5px dashed #1E3A5F;
    border-radius: 16px; padding: 8px; transition: all 0.3s;
}
[data-testid="stFileUploader"] * { color: #64748B !important; }
[data-testid="stFileUploader"] button {
    background: #1E3A5F !important; color: #93C5FD !important;
    border: none !important; border-radius: 8px !important;
}
.stTextInput input {
    background: #0D1421 !important; border: 1.5px solid #1E2D4A !important;
    border-radius: 12px !important; color: #E2E8F0 !important;
    font-size: 0.95rem !important; padding: 14px 18px !important;
}
.stTextInput input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
.stTextInput input::placeholder { color: #2D3D52 !important; }
.stTextInput label { display: none !important; }
.stButton > button {
    background: linear-gradient(135deg,#2563EB,#1D4ED8) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 10px 20px !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
}
[data-testid="stExpander"] {
    background: #0D1421 !important; border: 1px solid #1E2D4A !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] p,
[data-testid="stExpander"] td,
[data-testid="stExpander"] th { color: #4A6080 !important; }
.hero-banner {
    background: linear-gradient(135deg,#0D1B35 0%,#0A1628 50%,#06101E 100%);
    border: 1px solid #1E3A5F; border-radius: 20px;
    padding: 36px 40px; margin-bottom: 28px;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.2);
    border-radius: 20px; padding: 4px 12px; font-size: 0.72rem;
    font-weight: 600; color: #60A5FA; letter-spacing: 0.04em; margin-bottom: 16px;
}
.hero-title {
    font-family: 'Playfair Display', serif; font-size: 2.6rem;
    font-weight: 800; color: #F1F5F9; margin: 0;
    line-height: 1.1; letter-spacing: -0.01em;
}
.hero-title span { color: #3B82F6; }
.hero-sub { font-size: 0.9rem; color: #4A6080; margin-top: 10px; line-height: 1.6; }
.section-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
    font-weight: 500; color: #2D4A6A; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 10px;
}
.answer-wrap {
    background: linear-gradient(145deg,#0D1827,#0A1220);
    border: 1px solid #1E3050; border-radius: 16px;
    padding: 28px; margin-top: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.conf-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 16px; border-radius: 20px; font-size: 0.72rem;
    font-weight: 700; letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace; margin-bottom: 12px;
}
.badge-high { background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); color:#34D399; }
.badge-med  { background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.25); color:#FBBF24; }
.badge-low  { background:rgba(239,68,68,0.1);  border:1px solid rgba(239,68,68,0.25);  color:#F87171; }
.badge-desc { font-size:0.75rem; color:#2D4A6A; margin-bottom:20px; }
.ans-label {
    font-family:'JetBrains Mono',monospace; font-size:0.65rem;
    color:#2D4A6A; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:10px;
}
.ans-text { font-size:1.05rem; color:#CBD5E1; line-height:1.75; }
.src-card {
    background:rgba(14,165,233,0.05); border:1px solid rgba(14,165,233,0.15);
    border-left:3px solid #0EA5E9; border-radius:10px;
    padding:14px 18px; margin-top:20px;
}
.src-label {
    font-family:'JetBrains Mono',monospace; font-size:0.62rem;
    color:#0EA5E9; letter-spacing:0.1em; margin-bottom:6px;
}
.src-text { font-size:0.85rem; color:#7DD3FC; line-height:1.6; font-style:italic; }
.stat-chip {
    display:inline-flex; align-items:center; gap:6px;
    background:#0D1827; border:1px solid #1E3050; border-radius:8px;
    padding:5px 12px; font-family:'JetBrains Mono',monospace;
    font-size:0.72rem; color:#4A7FA5; margin:3px;
}
.stat-chip strong { color:#60A5FA; font-weight:600; }
.step-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:20px; }
.step-card {
    background:#0D1421; border:1px solid #1A2438;
    border-radius:12px; padding:18px;
}
.step-num {
    font-family:'Syne',sans-serif; font-size:1.4rem;
    font-weight:800; color:#1E3A5F; margin-bottom:10px;
}
.step-title { font-size:0.85rem; font-weight:600; color:#CBD5E1; margin-bottom:4px; }
.step-desc { font-size:0.75rem; color:#334155; line-height:1.4; }
.upload-hero {
    background:linear-gradient(135deg,#0A1628 0%,#080C14 100%);
    border:1.5px dashed #1E3A5F; border-radius:20px;
    padding:48px 32px; text-align:center; margin-bottom:28px;
}
.hist-item {
    background:#0A0F1A; border:1px solid #131D2E;
    border-radius:10px; padding:14px 18px; margin-bottom:8px;
}
.hist-q { font-size:0.85rem; font-weight:600; color:#94A3B8; }
.hist-a { font-size:0.78rem; color:#334155; margin-top:5px; }
[data-testid="stMetricValue"] {
    font-family:'JetBrains Mono',monospace !important;
    color:#60A5FA !important; font-size:0.9rem !important;
}
[data-testid="stMetricLabel"] {
    font-family:'JetBrains Mono',monospace !important;
    color:#2D4A6A !important; font-size:0.62rem !important;
    letter-spacing:0.08em !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────
for key, val in [("history",[]),("demo_mode", False),("collection",None),
                 ("doc_stats",{}),("total_tokens",0),
                 ("query_input","")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 24px 0;'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:1rem;
                    font-weight:700;color:#60A5FA;'>FinDoc</div>
        <div style='font-size:0.65rem;color:#1E3050;margin-top:2px;
                    font-family:"IBM Plex Mono",monospace;'>INTELLIGENCE v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    # ── DEMO BUTTON ─────────────────────────────────────────
    st.markdown("""
    <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;
                color:#1E3050;letter-spacing:0.1em;margin-bottom:10px;'>
        QUICK DEMO
    </div>""", unsafe_allow_html=True)

    if st.button("⚡  Load Demo Document", use_container_width=True):
        with st.spinner("Loading demo..."):
            import tempfile
            tmp = tempfile.NamedTemporaryFile(
                delete=False, suffix='.txt', mode='w', encoding='utf-8'
            )
            tmp.write(DEMO_DOC)
            tmp.close()
            from rag_pipeline import load_document, chunk_text, build_vector_store
            text   = load_document(tmp.name)
            chunks = chunk_text(text)
            col    = build_vector_store(chunks, "Meridian_Capital_2023")
            st.session_state.collection   = col
            st.session_state.doc_stats    = {
                "name"  : "Meridian Capital Annual Report 2023",
                "words" : len(text.split()),
                "chunks": len(chunks)
            }
            st.session_state.history      = []
            st.session_state.total_tokens = 0
            st.session_state.demo_mode    = True
        st.rerun()

    st.markdown("""
    <div style='font-size:0.68rem;color:#1E3050;margin:8px 0 20px;
                font-family:"IBM Plex Mono",monospace;'>
        Pre-loaded financial report · No upload needed
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;
                color:#1E3050;letter-spacing:0.1em;margin-bottom:10px;'>
        OR UPLOAD YOUR OWN
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload", type=["pdf","txt"], label_visibility="collapsed"
    )

    if uploaded:
        with st.spinner("Indexing..."):
            suffix = ".pdf" if uploaded.name.endswith(".pdf") else ".txt"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.read()); tmp.flush(); tmp.close()
            from rag_pipeline import load_document, chunk_text, build_vector_store
            text   = load_document(tmp.name)
            chunks = chunk_text(text)
            col    = build_vector_store(chunks, uploaded.name)
            st.session_state.collection   = col
            st.session_state.doc_stats    = {
                "name"  : uploaded.name,
                "words" : len(text.split()),
                "chunks": len(chunks)
            }
            st.session_state.history      = []
            st.session_state.total_tokens = 0
            st.session_state.demo_mode    = False
        st.success("Document ready ✓")

    if st.session_state.doc_stats:
        ds   = st.session_state.doc_stats
        name = (ds['name'][:22]+"...") if len(ds['name'])>22 else ds['name']
        demo = st.session_state.get("demo_mode", False)
        st.markdown(f"""
        <div style='margin-top:16px;padding:16px;background:#0D1421;
                    border:1px solid {"rgba(16,185,129,0.3)" if demo else "#1A2438"};
                    border-radius:12px;'>
            <div style='font-size:0.7rem;color:{"#34D399" if demo else "#60A5FA"};
                        font-weight:600;margin-bottom:6px;'>
                {"⚡ DEMO MODE" if demo else "📄"} {name}
            </div>
            <span class='stat-chip'><strong>{ds['words']:,}</strong> words</span>
            <span class='stat-chip'><strong>{ds['chunks']}</strong> chunks</span>
            <span class='stat-chip'>
                <strong>{st.session_state.total_tokens:,}</strong> tokens
            </span>
        </div>""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <div class='hero-badge'>⚡ RAG-POWERED · LLM EVALUATED</div>
    <div class='hero-title'>FinDoc <span>Intelligence</span></div>
    <div class='hero-sub'>
        Upload any financial document · Get grounded, cited answers
        with confidence scoring · Zero hallucinations guaranteed
    </div>
</div>
""", unsafe_allow_html=True)

# ── NO DOC ───────────────────────────────────────────────────
if not st.session_state.collection:
    st.markdown("""
    <div class='upload-hero'>
        <div style='font-size:3rem;margin-bottom:16px;'>📂</div>
        <div style='font-family:"Syne",sans-serif;font-size:1.3rem;
                    font-weight:700;color:#CBD5E1;margin-bottom:8px;'>
            No document loaded
        </div>
        <div style='font-size:0.85rem;color:#2D4A6A;margin-bottom:24px;'>
            Upload a PDF or TXT from the sidebar to begin
        </div>
        <span style='background:#0D1827;border:1px solid #1E3050;
                     padding:6px 14px;border-radius:8px;margin:4px;
                     font-size:0.75rem;color:#3B82F6;
                     font-family:"JetBrains Mono",monospace;
                     display:inline-block;'>Annual Reports</span>
        <span style='background:#0D1827;border:1px solid #1E3050;
                     padding:6px 14px;border-radius:8px;margin:4px;
                     font-size:0.75rem;color:#3B82F6;
                     font-family:"JetBrains Mono",monospace;
                     display:inline-block;'>Earnings Releases</span>
        <span style='background:#0D1827;border:1px solid #1E3050;
                     padding:6px 14px;border-radius:8px;margin:4px;
                     font-size:0.75rem;color:#3B82F6;
                     font-family:"JetBrains Mono",monospace;
                     display:inline-block;'>Loan Agreements</span>
        <span style='background:#0D1827;border:1px solid #1E3050;
                     padding:6px 14px;border-radius:8px;margin:4px;
                     font-size:0.75rem;color:#3B82F6;
                     font-family:"JetBrains Mono",monospace;
                     display:inline-block;'>SEC Filings</span>
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
            <div class='step-desc'>Chunked and embedded instantly</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>03</div>
            <div class='step-title'>Ask</div>
            <div class='step-desc'>Revenue, margins, debt, risks</div>
        </div>
        <div class='step-card'>
            <div class='step-num'>04</div>
            <div class='step-title'>Answer</div>
            <div class='step-desc'>Cited and confidence-scored</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Q&A ──────────────────────────────────────────────────────
st.markdown("<div class='section-label'>Suggested Queries</div>",
            unsafe_allow_html=True)

suggestions = [
    "What was the total revenue?",
    "What is the net income margin?",
    "What is the debt position?",
    "What are the main risk factors?",
]
c1, c2, c3, c4 = st.columns(4)
for col, sug in zip([c1,c2,c3,c4], suggestions):
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
    st.session_state.history.append(
        {"query":query,"result":result,"elapsed":elapsed}
    )

# ── ANSWER ───────────────────────────────────────────────────
if st.session_state.history:
    latest = st.session_state.history[-1]
    r      = latest["result"]
    conf   = r["confidence"]
    sim    = round(r["similarity"], 3)

    badge_map = {
        "HIGH":  ("badge-high","● HIGH CONFIDENCE",
                  "Strong semantic match · Answer is reliable"),
        "MEDIUM":("badge-med", "● MEDIUM CONFIDENCE",
                  "Related context found · Verify numerical data"),
        "LOW":   ("badge-low", "● LOW CONFIDENCE — FALLBACK",
                  "Insufficient context · LLM skipped · No hallucination risk"),
    }
    bcss, blabel, bdesc = badge_map[conf]
    ans = r["answer"].replace("<","&lt;").replace(">","&gt;")

    # Answer card — open
    st.markdown("<div class='answer-wrap'>", unsafe_allow_html=True)

    # Badge
    st.markdown(
        f"<span class='conf-badge {bcss}'>{blabel}</span>"
        f"<div class='badge-desc'>{bdesc}</div>",
        unsafe_allow_html=True
    )

    # Answer text
    st.markdown(
        f"<div class='ans-label'>Response</div>"
        f"<div class='ans-text'>{ans}</div>",
        unsafe_allow_html=True
    )

    # Source
    if r["source"] not in ["No relevant section found.",
                            "See document context."]:
        src = r["source"].replace("<","&lt;").replace(">","&gt;")
        st.markdown(
            f"<div class='src-card'>"
            f"<div class='src-label'>📎 SOURCE CITATION</div>"
            f"<div class='src-text'>{src}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Metrics
    st.markdown("<div style='height:16px'></div>",
                unsafe_allow_html=True)
    m1,m2,m3,m4,m5 = st.columns(5)
    m1.metric("CONFIDENCE",  conf)
    m2.metric("SIMILARITY",  str(sim))
    m3.metric("CHUNKS USED", str(r["chunks_used"]))
    m4.metric("TOKENS",      str(r["tokens_used"]))
    m5.metric("LATENCY",     f"{latest['elapsed']}s")

    # Card close
    st.markdown("</div>", unsafe_allow_html=True)

# ── HISTORY ──────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown("<div style='height:28px'></div>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Query History</div>",
                unsafe_allow_html=True)

    icons = {"HIGH":"🟢","MEDIUM":"🟡","LOW":"🔴"}
    for item in reversed(st.session_state.history[:-1]):
        r   = item["result"]
        ans = r["answer"][:130].replace(
            "<","&lt;").replace(">","&gt;")
        st.markdown(
            f"<div class='hist-item'>"
            f"<div class='hist-q'>{icons[r['confidence']]} &nbsp;"
            f"{item['query']}</div>"
            f"<div class='hist-a'>{ans}...</div>"
            f"</div>",
            unsafe_allow_html=True
        )