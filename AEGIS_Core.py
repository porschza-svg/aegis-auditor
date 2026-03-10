import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# PAGE CONFIG
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | WAT SYSTEMS",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# ── Premium Dark Theme (X + Tesla 2026 vibe) ──
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main, .stApp { background-color: #000000; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    hr { border-color: #1a1a1a; margin: 3rem 0; }

    /* Typography */
    h1, h2, h3 { font-weight: 600; letter-spacing: -0.02em; }
    p, li { line-height: 1.75; color: #d1d5db; }
    code, pre { font-family: 'JetBrains Mono', monospace; background: #0d0d0d; border: 1px solid #1f1f1f; }

    /* Header */
    .header { padding: 6rem 0 3rem; text-align: center; }
    .logo { font-size: 7.5rem; font-weight: 900; letter-spacing: -0.08em; color: #ffffff; line-height: 0.85; margin: 0; }
    .subtitle { font-size: 1.05rem; font-weight: 400; color: #6b7280; letter-spacing: 0.3em; text-transform: uppercase; margin-top: 1.5rem; }

    /* Modules */
    .modules { display: flex; justify-content: center; gap: 2.5rem; margin: 3rem 0 5rem; flex-wrap: wrap; }
    .module { background: #0a0a0a; border: 1px solid #1f1f1f; border-radius: 1.25rem; padding: 2rem 2.5rem; min-width: 240px; text-align: center; transition: all 0.3s ease; }
    .module:hover { border-color: #3b82f6; box-shadow: 0 0 30px rgba(59,130,246,0.1); }
    .mod-status { font-size: 0.85rem; color: #10b981; font-weight: 600; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.8rem; }
    .mod-name { font-size: 1.2rem; font-weight: 600; color: #f3f4f6; }

    /* Textarea */
    .stTextArea textarea { 
        background: #0a0a0a !important; 
        border: 1px solid #1f1f1f !important; 
        border-radius: 1.25rem !important; 
        color: #e0e0e0 !important; 
        font-family: 'JetBrains Mono', monospace !important; 
        font-size: 1rem !important; 
        padding: 1.8rem !important; 
        line-height: 1.8; 
        min-height: 380px; 
    }
    .stTextArea textarea:focus { 
        border-color: #60a5fa !important; 
        box-shadow: 0 0 0 4px rgba(96,165,250,0.15) !important; 
    }

    /* Buttons - Modern Pill Style */
    div.stButton > button {
        border-radius: 9999px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 1rem 2.2rem !important;
        transition: all 0.3s ease;
        width: auto !important;
        min-width: 220px;
        margin: 0.5rem;
    }
    div.stButton > button[kind="primary"] {
        background: #1d4ed8 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(29,78,216,0.25);
    }
    div.stButton > button[kind="primary"]:hover {
        background: #3b82f6 !important;
        transform: translateY(-2px);
    }
    div.stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #93c5fd !important;
        border: 1px solid #374151 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #111 !important;
        color: white !important;
    }

    /* Result Box */
    .result-box { 
        background: #050505; 
        border: 1px solid #1f1f1f; 
        border-radius: 1.5rem; 
        padding: 3.5rem 3rem; 
        margin: 3rem 0; 
    }
    .score-label { font-size: 1rem; color: #6b7280; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 1rem; }
    .score-big { font-size: 8rem; font-weight: 900; color: #ffffff; letter-spacing: -0.06em; line-height: 0.9; margin: 0.5rem 0 1.5rem; }
    .badge { background: #111; color: #93c5fd; padding: 0.5rem 1.4rem; border-radius: 9999px; font-size: 0.9rem; font-weight: 600; }

    /* Findings */
    .finding { 
        background: #0a0a0a; 
        border: 1px solid #1f1f1f; 
        border-left: 4px solid #ef4444; 
        border-radius: 1rem; 
        padding: 2rem; 
        margin: 2rem 0; 
        transition: all 0.25s; 
    }
    .finding:hover { border-left-color: #f87171; box-shadow: 0 6px 25px rgba(239,68,68,0.08); }
    .issue-num { font-size: 0.9rem; color: #f87171; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 1rem; }
    .issue-title { font-size: 1.4rem; font-weight: 600; color: #f3f4f6; margin-bottom: 1rem; }
    .impact { font-size: 1.05rem; color: #d1d5db; line-height: 1.8; }

    /* Locked Pill */
    .locked-pill { 
        background: #111827; 
        border: 1px solid #374151; 
        border-radius: 9999px; 
        padding: 1.4rem 3rem; 
        text-align: center; 
        margin: 2.5rem 0; 
        font-weight: 600; 
        color: #fbbf24; 
        font-size: 1.05rem; 
        letter-spacing: 0.1em; 
    }

    /* Share */
    .share-btn { 
        display: inline-block; 
        background: transparent; 
        border: 1px solid #374151; 
        color: #e0e0e0 !important; 
        padding: 1rem 2.5rem; 
        border-radius: 9999px; 
        text-decoration: none; 
        font-weight: 600; 
        transition: all 0.3s; 
    }
    .share-btn:hover { background: #1d4ed8; border-color: #1d4ed8; color: #fff !important; }

    /* Footer */
    .footer { text-align: center; color: #4b5563; font-size: 0.95rem; margin: 7rem 0 4rem; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# TELEGRAM RADAR
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS* {status} | Score: {score}% | Issues: {issues_count} 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# SUPREME ENGINE
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: 
        return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    last_err = ""
    for model in model_pool:
        try:
            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "system", "content": "You are AEGIS, the supreme Logic Auditor. Identify ALL structural and logic vulnerabilities. Be factual, professional, and brutal. Provide a detailed multi-point audit. Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                                 {"role": "user", "content": payload[:12000]}],
                    "temperature": 0.0,
                    "response_format": {"type": "json_object"}
                }), timeout=40
            )
            if resp.status_code == 200:
                result = json.loads(resp.json()['choices'][0]['message']['content'])
                send_radar(result.get('trust_score', 0), len(result.get('findings', [])))
                return result
            last_err = resp.text
        except Exception as e: last_err = str(e)
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Verify API Status."}]}

# ────────────────────────────────────────────────
# INTERFACE
# ────────────────────────────────────────────────
st.markdown("""
    <div class="header">
        <div class="logo">AEGIS</div>
        <div class="subtitle">WAT SYSTEMS — Universal Logic Authority</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="modules">
        <div class="module"><span class="mod-status">OPERATIONAL</span><div class="mod-name">CODE SECURITY</div></div>
        <div class="module"><span class="mod-status">OPERATIONAL</span><div class="mod-name">WORKFLOW LOGIC</div></div>
        <div class="module"><span class="mod-status">OPERATIONAL</span><div class="mod-name">SMART CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("PASTE YOUR LOGIC / CODE / ARCHITECTURE", height=400,
                       placeholder="Smart contract, Python/JS code, workflow description, or full system spec...")

if st.button("EXECUTE AUDIT", type="primary"):
    if not payload.strip():
        st.error("No payload provided.")
    else:
        with st.spinner("Auditing..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# RESULT SECTION
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)

    st.markdown("<div class='result-box'>", unsafe_allow_html=True)

    st.markdown(f"<div class='score-label'>TRUST SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-big'>{score}</div>", unsafe_allow_html=True)
    st.markdown("<div class='badge'>AEGIS VALIDATED</div>", unsafe_allow_html=True)

    share_msg = f"AEGIS audit: {score}% trust score | WAT SYSTEMS 🛡️"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div style='text-align:center; margin:3rem 0;'><a href='{share_url}' target='_blank' class='share-btn'>Share on 𝕏</a></div>", unsafe_allow_html=True)

    st.markdown("<h2 style='margin:4rem 0 2rem;'>Detected Vulnerabilities</h2>", unsafe_allow_html=True)

    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class="finding">
                <span class="issue-num">ISSUE {i+1:02}</span>
                <div class="issue-title">{f.get('issue')}</div>
                <div class="impact"><strong>Impact:</strong> {f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.unlocked:
            st.markdown("<div class='locked-pill'>FULL REMEDIATION LOCKED</div>", unsafe_allow_html=True)
        else:
            st.success("**Remediation**")
            st.code(f.get('the_cure'), language='python')

    # Unlock + New Audit Buttons - จัดกลุ่มสวย ๆ
    st.markdown("<div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin: 4rem 0;'>", unsafe_allow_html=True)

    if not st.session_state.unlocked:
        st.link_button(
            "UNLOCK FULL ACCESS — $9",
            "https://porschza.gumroad.com/l/AEGIS",
            type="primary",
            use_container_width=False
        )

        col_pass, col_btn = st.columns([2.5, 1])
        with col_pass:
            passcode = st.text_input("Or enter passcode", type="password", key="unlock_input")
        with col_btn:
            if st.button("UNLOCK", type="primary"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else:
                    st.error("Access denied.")

    if st.button("START NEW AUDIT", type="secondary"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.session_state.unlocked = False
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>WAT SYSTEMS | AEGIS v32.3 © 2026</div>", unsafe_allow_html=True)
