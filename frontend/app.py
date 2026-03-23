import streamlit as st
import requests
import PyPDF2

from summarizer import generate_summary
from paraphraser import paraphrase_text
from readability import get_readability
from pdf_qa import answer_question

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="TextMorph AI", layout="wide", page_icon="🧠")

# ================= CUSTOM UI =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #07090F !important;
    color: #CBD5E1 !important;
}

.main, .block-container, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #07090F !important;
}

[data-testid="stHeader"] {
    background-color: #07090F !important;
    border-bottom: 1px solid #1A2030;
}

.block-container {
    padding: 2.5rem 3rem;
    max-width: 1200px;
    background-color: #07090F !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #2D3748; border-radius: 3px; }

/* ── Header ── */
.tm-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1A2030;
}

.tm-logo {
    width: 46px;
    height: 46px;
    background: linear-gradient(135deg, #6EE7F7, #818CF8);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.tm-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #E2E8F0, #94A3B8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1;
}

.tm-subtitle {
    font-size: 13px;
    color: #4A5568;
    margin: 4px 0 0 0;
    font-weight: 300;
    letter-spacing: 0.5px;
}

/* ── Cards ── */
.card {
    background: #0D1117;
    border: 1px solid #1A2030;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #6EE7F720, #818CF820, transparent);
}

/* ── Section Labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4A5568;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1A2030;
}

/* ── Output box ── */
.output-box {
    background: #0A0E16;
    border: 1px solid #1E2A3A;
    border-radius: 10px;
    padding: 18px;
    font-size: 14px;
    line-height: 1.7;
    color: #CBD5E1;
}

/* ── Metric tiles ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
    margin-top: 4px;
}

.metric-tile {
    background: #0A0E16;
    border: 1px solid #1E2A3A;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #6EE7F7;
    line-height: 1;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 11px;
    color: #4A5568;
    letter-spacing: 0.5px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6EE7F7, #818CF8) !important;
    color: #07090F !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    transition: opacity 0.2s, transform 0.15s !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── History buttons ── */
.stSidebar .stButton > button {
    background: #0D1117 !important;
    color: #CBD5E1 !important;
    border: 1px solid #1A2030 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    width: 100% !important;
    margin-bottom: 4px !important;
    transition: border-color 0.2s, background 0.2s !important;
}

.stSidebar .stButton > button:hover {
    background: #131B2A !important;
    border-color: #6EE7F740 !important;
    color: #E2E8F0 !important;
}

/* New Analysis button - first button in sidebar gets accent style */
.stSidebar .stButton:first-of-type > button {
    background: linear-gradient(135deg, #6EE7F715, #818CF815) !important;
    border: 1px solid #6EE7F730 !important;
    color: #6EE7F7 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    text-align: center !important;
    margin-bottom: 8px !important;
}

.stSidebar .stButton:first-of-type > button:hover {
    background: linear-gradient(135deg, #6EE7F725, #818CF725) !important;
    border-color: #6EE7F760 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0A0E16 !important;
    border: 1px solid #1E2A3A !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6EE7F740 !important;
    box-shadow: 0 0 0 3px #6EE7F710 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #0A0E16 !important;
    border: 1px solid #1E2A3A !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0A0E16;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #1A2030;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #4A5568;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    padding: 8px 18px;
}

.stTabs [aria-selected="true"] {
    background: #1A2030 !important;
    color: #E2E8F0 !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    background: linear-gradient(135deg, #0D1320, #0A0E16) !important;
    border: 1.5px dashed #2D3F55 !important;
    border-radius: 14px !important;
    transition: border-color 0.25s, background 0.25s !important;
}

.stFileUploader > div:hover {
    border-color: #6EE7F760 !important;
    background: linear-gradient(135deg, #0D1828, #0C1219) !important;
}

.stFileUploader label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #4A6080 !important;
}

/* Native drag-and-drop bar */
.stFileUploader [data-testid="stFileUploaderDropzone"] {
    background: #0A0E16 !important;
    border: none !important;
    border-top: 1px solid #1A2030 !important;
    border-radius: 0 0 14px 14px !important;
    padding: 10px 16px !important;
}

.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
    color: #334155 !important;
    font-size: 12px !important;
}

.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #334155 !important;
}

.stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] svg {
    fill: #2D3F55 !important;
}

.stFileUploader button {
    background: linear-gradient(135deg, #6EE7F718, #818CF818) !important;
    border: 1px solid #2D3F55 !important;
    border-radius: 8px !important;
    color: #6EE7F7 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    letter-spacing: 0.5px !important;
    transition: background 0.2s !important;
}

.stFileUploader button:hover {
    background: linear-gradient(135deg, #6EE7F730, #818CF730) !important;
    border-color: #6EE7F760 !important;
}

.uploadedFile {
    background: #0D1320 !important;
    border: 1px solid #1E2A3A !important;
    border-radius: 8px !important;
    color: #CBD5E1 !important;
    font-size: 12px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0A0E16 !important;
    border-right: 1px solid #1A2030 !important;
}

.sidebar-user {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 16px;
    background: #0D1117;
    border: 1px solid #1A2030;
    border-radius: 12px;
    margin-bottom: 20px;
}

.sidebar-avatar {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, #6EE7F7, #818CF8);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
}

.sidebar-name {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #E2E8F0;
}

.sidebar-role {
    font-size: 11px;
    color: #4A5568;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.history-item {
    background: #0D1117;
    border: 1px solid #1A2030;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 2px;
    transition: border-color 0.2s;
}

.history-item:hover {
    border-color: #2D3A50;
}

.history-filename {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: #CBD5E1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.history-actions {
    display: flex;
    gap: 6px;
    margin-top: 6px;
}

/* ── History action buttons ── */
.stSidebar .stButton > button {
    background: #0D1117 !important;
    color: #64748B !important;
    border: 1px solid #1A2030 !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 6px 10px !important;
    width: 100% !important;
    margin-bottom: 4px !important;
    transition: border-color 0.2s, background 0.2s !important;
    text-align: left !important;
}

.stSidebar .stButton > button:hover {
    background: #131B2A !important;
    border-color: #6EE7F740 !important;
    color: #CBD5E1 !important;
}

/* New Analysis button */
.stSidebar .stButton:first-of-type > button {
    background: linear-gradient(135deg, #6EE7F715, #818CF815) !important;
    border: 1px solid #6EE7F730 !important;
    color: #6EE7F7 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    text-align: center !important;
    width: 100% !important;
    padding: 8px 12px !important;
    margin-bottom: 4px !important;
}

.stSidebar .stButton:first-of-type > button:hover {
    background: linear-gradient(135deg, #6EE7F725, #818CF725) !important;
    border-color: #6EE7F760 !important;
}

/* Logout button */
.stSidebar .stButton:nth-of-type(2) > button {
    background: transparent !important;
    border: 1px solid #1A2030 !important;
    color: #4A5568 !important;
    font-size: 12px !important;
    width: 100% !important;
    padding: 7px 12px !important;
    margin-bottom: 8px !important;
}

.stSidebar .stButton:nth-of-type(2) > button:hover {
    border-color: #EF444430 !important;
    color: #EF4444 !important;
    background: #EF444408 !important;
}

/* ── Success / info ── */
.stSuccess, .stInfo {
    background: #0A0E16 !important;
    border: 1px solid #1E2A3A !important;
    border-radius: 10px !important;
    color: #6EE7F7 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #6EE7F7 !important;
}

/* ── Login page ── */
.login-wrap {
    max-width: 420px;
    margin: 60px auto 0;
}

.login-card {
    background: #0D1117;
    border: 1px solid #1A2030;
    border-radius: 20px;
    padding: 36px 32px;
    position: relative;
    overflow: hidden;
}

.login-card::before {
    content: '';
    position: absolute;
    top: -80px; left: -80px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, #6EE7F710 0%, transparent 70%);
    pointer-events: none;
}

.login-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #E2E8F0;
    margin-bottom: 4px;
}

.login-sub {
    font-size: 13px;
    color: #4A5568;
    margin-bottom: 28px;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "selected_history" not in st.session_state:
    st.session_state.selected_history = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "para" not in st.session_state:
    st.session_state.para = None
if "scores" not in st.session_state:
    st.session_state.scores = None
if "qa_answer" not in st.session_state:
    st.session_state.qa_answer = None
if "source_name" not in st.session_state:
    st.session_state.source_name = "Pasted Text"
if "display_name" not in st.session_state:
    st.session_state.display_name = ""


# ================= LOGIN =================
if st.session_state.user is None:
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown("""
        <div class="login-card">
            <div class="login-title">🧠 TextMorph AI</div>
            <div class="login-sub">Sign in to continue</div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        role = st.selectbox("Role", ["User", "Admin"])
        email = st.text_input("Email", placeholder="Enter your email")
        if role == "User":
            display_name = st.text_input("Username", placeholder="Enter your display name")
        else:
            display_name = ""
        password = st.text_input("Password", placeholder="Enter password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            create_clicked = st.button("Create Account", use_container_width=True, disabled=(role != "User"))
            if create_clicked and role == "User":
                if not email or not password or not display_name:
                    st.markdown('<p style="color:#EF4444;font-size:12px;margin:4px 0;">⚠ Please fill in all fields to create an account.</p>', unsafe_allow_html=True)
                else:
                    res = requests.post(f"{API_URL}/signup", json={"username": email, "password": password, "display_name": display_name})
                    result = res.json()
                    if result.get("status") == "success":
                        st.markdown('<p style="color:#6EE7F7;font-size:12px;margin:4px 0;">✅ Account created! You can now sign in.</p>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p style="color:#EF4444;font-size:12px;margin:4px 0;">⚠ This email is already registered.</p>', unsafe_allow_html=True)
        with col2:
            if st.button("Sign In →", use_container_width=True):
                if not email or not password:
                    st.markdown('<p style="color:#EF4444;font-size:12px;margin:4px 0;">⚠ Please enter your email and password.</p>', unsafe_allow_html=True)
                elif role == "Admin":
                    if email == "admin" and password == "admin123":
                        st.session_state.user = "admin"
                        st.session_state.display_name = "Admin"
                        st.session_state.role = "admin"
                        st.rerun()
                    else:
                        st.markdown('<p style="color:#EF4444;font-size:12px;margin:4px 0;">⚠ Invalid admin credentials.</p>', unsafe_allow_html=True)
                else:
                    res = requests.post(f"{API_URL}/login", json={"username": email, "password": password})
                    if res.json()["status"] == "success":
                        st.session_state.user = email
                        st.session_state.display_name = res.json().get("display_name", email)
                        st.session_state.role = "user"
                        st.rerun()
                    else:
                        st.markdown('<p style="color:#EF4444;font-size:12px;margin:4px 0;">⚠ Incorrect email or password.</p>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ================= SIDEBAR =================

# ── TOP: Account ──
st.sidebar.markdown(f"""
<div class="sidebar-user">
    <div class="sidebar-avatar">{'👑' if st.session_state.role == 'admin' else '👤'}</div>
    <div>
        <div class="sidebar-name">{st.session_state.display_name or st.session_state.user}</div>
        <div class="sidebar-role">{st.session_state.role}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── New Analysis + Logout below account ──
if st.sidebar.button("＋  New Analysis", key="new_analysis", use_container_width=True):
    st.session_state.selected_history = None
    st.session_state.summary = None
    st.session_state.para = None
    st.session_state.scores = None
    st.session_state.qa_answer = None
    st.session_state.source_name = "Pasted Text"
    st.rerun()

if st.sidebar.button("🚪  Logout", key="logout_btn", use_container_width=True):
    st.session_state.user = None
    st.rerun()

st.sidebar.markdown("---")


# ================= USER DASHBOARD =================
if st.session_state.role == "user":

    # Header
    st.markdown("""
    <div class="tm-header">
        <div class="tm-logo">🧠</div>
        <div>
            <div class="tm-title">TextMorph AI</div>
            <div class="tm-subtitle">Summarize · Paraphrase · Analyze · Ask</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INPUT CARD ──
    st.markdown('<div class="card">', unsafe_allow_html=True)

    text = ""

    st.markdown('<div class="section-label">Type or Paste Text</div>', unsafe_allow_html=True)
    t = st.text_area("Input text", placeholder="Type or paste your text here...", height=180, label_visibility="hidden")
    if t:
        text = t
        st.session_state.source_name = "Pasted Text"

    st.markdown('<div class="section-label" style="margin-top:16px;">Upload File</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0D1320, #0A0E16);
        border: 1.5px dashed #2D3F55;
        border-radius: 14px;
        padding: 22px 20px 10px 20px;
        margin-bottom: -12px;
        text-align: center;
    ">
        <div style="font-size:28px; margin-bottom:6px;">📂</div>
        <div style="font-family:'Syne',sans-serif; font-size:13px; font-weight:700; color:#CBD5E1; margin-bottom:4px;">
            Drop your file here
        </div>
        <div style="font-size:11px; color:#334155; letter-spacing:0.5px;">
            Supports PDF &amp; TXT &nbsp;·&nbsp; Max 200MB
        </div>
    </div>
    """, unsafe_allow_html=True)
    file = st.file_uploader("Upload file", type=["txt", "pdf"], label_visibility="hidden")
    if file:
        st.session_state.source_name = file.name
        if file.type == "text/plain":
            text = file.read().decode("utf-8")
        else:
            pdf = PyPDF2.PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() or ""

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        summary_level = st.selectbox("Summary Length", ["Short", "Medium", "Long"])
    with col2:
        para_level = st.selectbox("Paraphrase Style", ["Beginner", "Intermediate", "Advanced"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button("⚡  Analyze")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── OUTPUT ──
    if analyze and text.strip():
        with st.spinner("Analyzing your text..."):
            st.session_state.scores = get_readability(text)
            st.session_state.summary = generate_summary(text, summary_level)
            st.session_state.para = paraphrase_text(text, para_level)
            requests.post(f"{API_URL}/save", json={
                "username": st.session_state.user,
                "text": text,
                "summary": st.session_state.summary,
                "paraphrase": st.session_state.para,
                "source_name": st.session_state.source_name
            })

    if "summary" in st.session_state and st.session_state.summary:
        # ── READABILITY ──
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Readability Scores</div>', unsafe_allow_html=True)

        tiles_html = '<div class="metric-grid">'
        for key, val in st.session_state.scores.items():
            label = key.replace("_", " ").title()
            display = round(val, 1) if isinstance(val, float) else val
            tiles_html += f"""
            <div class="metric-tile">
                <div class="metric-value">{display}</div>
                <div class="metric-label">{label}</div>
            </div>"""
        tiles_html += '</div>'
        st.markdown(tiles_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── SUMMARY + PARAPHRASE ──
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Paraphrase</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{st.session_state.para}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── PDF Q&A ──
    if text:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Ask a Question</div>', unsafe_allow_html=True)

        q = st.text_input("Question", placeholder="Ask anything about your text...", label_visibility="hidden")
        if st.button("Get Answer"):
            if q:
                st.session_state.qa_answer = answer_question(text, q)

        if "qa_answer" in st.session_state and st.session_state.qa_answer:
            st.markdown(f'<div class="output-box">💬 {st.session_state.qa_answer}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── SIDEBAR HISTORY ──
    st.sidebar.markdown('<div class="section-label" style="margin-top:16px;">History</div>', unsafe_allow_html=True)

    try:
        res = requests.get(f"{API_URL}/history/{st.session_state.user}")
        history = res.json()
    except Exception as e:
        history = []
        st.sidebar.error("Could not load history")

    if not history:
        st.sidebar.markdown('<div style="font-size:11px;color:#334155;padding:8px 4px;">No history yet.</div>', unsafe_allow_html=True)

    for i, item in enumerate(history[::-1]):
        name = item.get("source_name") or "Pasted Text"
        if name.endswith(".pdf"):
            icon = "📄"
        elif name.endswith(".txt"):
            icon = "📝"
        else:
            icon = "✏️"

        c1, c2 = st.sidebar.columns([5, 1])
        with c1:
            if st.button(f"{icon}  {name}", key=f"hist_{i}", use_container_width=True):
                st.session_state.selected_history = item
                st.session_state.summary = None
                st.session_state.para = None
                st.session_state.scores = None
                st.session_state.qa_answer = None
                st.rerun()
        with c2:
            item_id = item.get("id")
            if item_id and st.button("🗑", key=f"del_{i}", use_container_width=True):
                requests.delete(f"{API_URL}/history/{item_id}")
                if st.session_state.selected_history and st.session_state.selected_history.get("id") == item_id:
                    st.session_state.selected_history = None
                st.rerun()

    # ── HISTORY DETAIL VIEW ──
    if st.session_state.selected_history:
        item = st.session_state.selected_history
        name = item.get("source_name") or "Pasted Text"

        st.markdown(f"""
        <div class="tm-header" style="margin-top:10px;">
            <div class="tm-logo">🕘</div>
            <div>
                <div class="tm-title">{name}</div>
                <div class="tm-subtitle">History Detail</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{item.get("summary", "N/A")}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Paraphrase</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="output-box">{item.get("paraphrase", "N/A")}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Original Text</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{item.get("text", "N/A")[:1000]}{"..." if len(item.get("text","")) > 1000 else ""}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_back, col_del = st.columns([3, 1])
        with col_back:
            if st.button("← Back to Analyze"):
                st.session_state.selected_history = None
                st.rerun()
        with col_del:
            if st.button("🗑 Delete this record"):
                requests.delete(f"{API_URL}/history/{item['id']}")
                st.session_state.selected_history = None
                st.rerun()


# ================= ADMIN =================
elif st.session_state.role == "admin":

    st.markdown("""
    <div class="tm-header">
        <div class="tm-logo">👑</div>
        <div>
            <div class="tm-title">Admin Dashboard</div>
            <div class="tm-subtitle">Manage users and system settings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Status</div>', unsafe_allow_html=True)
    st.info("Admin features coming soon...")
    st.markdown('</div>', unsafe_allow_html=True)