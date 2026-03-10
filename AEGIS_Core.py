import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. ENTERPRISE DESIGN SYSTEM (PREMIUM 2026)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | WAT SYSTEMS",
    layout="wide",  # เปลี่ยนเป็น wide เพื่อให้ดูโปรกว้างขึ้น
    page_icon="🛡️",
    initial_sidebar_state="collapsed"  # Sidebar พับไว้ก่อน ดูสะอาด
)

# Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# ── Premium Obsidian-Inspired Dark Theme ──
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #0a0a0a; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0a; }

    /* Typography */
    h1, h2, h3 { font-weight: 700; letter-spacing: -0.025em; }
    code, pre { font-family: 'JetBrains Mono', monospace; }

    /* Header */
    .header-container {
        padding: 6rem 0 4rem;
        text-align: center;
        border-bottom: 1px solid #1f2937;
        margin-bottom: 3rem;
    }
    .brand-logo {
        font-size: 6.5rem;
        font-weight: 900;
        letter-spacing: -0.12em;
        color: #ffffff;
        line-height: 0.85;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 1.1rem;
        font-weight: 500;
        color: #64748b;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 1.5rem;
        opacity: 0.9;
    }

    /* Module Grid */
    .module-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0 5rem;
    }
    .module-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 1rem;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .module-card:hover {
        border-color: #3b82f6;
        transform: translateY(-6px);
        box-shadow: 0 20px 35px -10px rgba(59,130,246,0.18);
    }
    .module-status {
        font-size: 0.85rem;
        font-weight: 700;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: block;
        margin-bottom: 0.75rem;
    }
    .module-name {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
    }

    /* Textarea - Terminal Style */
    .stTextArea textarea {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 1rem !important;
        color: #e2e8f0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1rem !important;
        padding: 1.8rem !important;
        line-height: 1.7;
        min-height: 380px;
        transition: all 0.25s;
    }
    .stTextArea textarea:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 4px rgba(96,165,250,0.2) !important;
    }

    /* Primary CTA Button */
    div.stButton > button[kind="primary"], div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border-radius: 1rem !important;
        padding: 1.4rem 0 !important;
        width: 100% !important;
        border: none !important;
        letter-spacing: 0.04em;
        transition: all 0.3s ease;
        box-shadow: 0 6px 12px -4px rgba(59,130,246,0.3);
        margin: 2rem 0 1rem;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) !important;
        transform: translateY(-4px);
        box-shadow: 0 15px 30px -8px rgba(59,130,246,0.45);
    }

    /* Result Container */
    .result-container {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 1.25rem;
        padding: 3.5rem 3rem;
        margin: 4rem 0;
    }
    .score-header {
        font-size: 1rem;
        font-weight: 600;
        color: #94a3b8;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .score-number {
        font-size: 10rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -0.1em;
        line-height: 0.8;
        margin: 0.5rem 0 1.5rem;
    }
    .validated-badge {
        background: #1e40af;
        color: #bfdbfe;
        padding: 0.5rem 1.25rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 700;
        display: inline-block;
    }

    /* Finding Cards */
    .finding-card {
        border-left: 5px solid #ef4444;
        background: #0f172a;
        border-radius: 0.75rem;
        padding: 2rem;
        margin: 2rem 0;
        transition: all 0.25s;
    }
    .finding-card:hover {
        border-left-color: #f87171;
        box-shadow: 0 8px 20px -6px rgba(239,68,68,0.15);
    }
    .finding-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #f87171;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: block;
    }
    .finding-issue {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 1rem;
    }
    .finding-impact {
        font-size: 1.1rem;
        color: #cbd5e1;
        line-height: 1.7;
    }

    /* Locked Section */
    .locked-section {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 3rem;
        text-align: center;
        margin: 2.5rem 0;
    }
    .locked-text {
        font-size: 1rem;
        font-weight: 700;
        color: #fbbf24;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    /* Share Button */
    .share-link {
        display: inline-block;
        background: transparent;
        border: 1px solid #475569;
        color: #e2e8f0 !important;
        padding: 1rem 2.5rem;
        border-radius: 1rem;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
    }
    .share-link:hover {
        background: #ffffff;
        color: #0f172a !important;
        border-color: #ffffff;
        transform: translateY(-3px);
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #475569;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 8rem 0 4rem;
        letter-spacing: 0.08em;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (unchanged)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *[AEGIS AUTHORITY]*\n\n● *Status:* {status}\n● *Score:* {score}%\n● *Findings:* {issues_count}\n\n📡 _WAT SYSTEMS_"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (unchanged)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

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
# 4. INTERFACE (upgraded layout)
# ────────────────────────────────────────────────
st.markdown("""
    <div class="header-container">
        <div class="brand-logo">AEGIS</div>
        <div class="brand-subtitle">WAT SYSTEMS — Universal Logic Authority</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="module-grid">
        <div class="module-card"><span class="module-status">OPERATIONAL</span><div class="module-name">CODE SECURITY</div></div>
        <div class="module-card"><span class="module-status">OPERATIONAL</span><div class="module-name">WORKFLOW LOGIC</div></div>
        <div class="module-card"><span class="module-status">OPERATIONAL</span><div class="module-name">SMART CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("ENTER TARGET LOGIC / SOURCE CODE / ARCHITECTURE", height=400,
                       placeholder="Paste your smart contract, Python/JS code, workflow description, or full architecture here...")

if st.button("EXECUTE SUPREME AUDIT", type="primary"):
    if not payload.strip():
        st.error("ERROR: No payload provided.")
    else:
        with st.spinner("Analyzing logic integrity..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (premium freemium display)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)

    st.markdown("<div class='result-container'>", unsafe_allow_html=True)

    col_score, col_badge = st.columns([4, 1])
    with col_score:
        st.markdown(f"<div class='score-header'>GLOBAL TRUST SCORE</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='score-number'>{score}</div>", unsafe_allow_html=True)
    with col_badge:
        st.markdown("<div style='padding-top:5rem;'><div class='validated-badge'>VALIDATED BY AEGIS CORE</div></div>", unsafe_allow_html=True)

    # Share
    share_msg = f"AEGIS audit complete: {score}% trust score | Verified by WAT SYSTEMS 🛡️"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"""
        <div style="text-align:center; margin:3rem 0;">
            <a href="{share_url}" target="_blank" class="share-link">SHARE RESULT ON 𝕏</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin:3rem 0 2rem; font-size:2rem;'>Detected Critical Vulnerabilities</h2>", unsafe_allow_html=True)

    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class="finding-card">
                <span class="finding-label">ISSUE {i+1:02}</span>
                <div class="finding-issue">{f.get('issue')}</div>
                <div class="finding-impact"><strong>Catastrophic Impact:</strong> {f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state.unlocked:
            st.markdown("""
                <div class="locked-section">
                    <span class="locked-text">🔒 FULL REMEDIATION LOCKED</span>
                    <p style="color:#94a3b8; margin-top:1rem;">Enterprise access required to view detailed fixes and code-level cures.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**Recommended Remediation**")
            st.code(f.get('the_cure'), language="python")

    if not st.session_state.unlocked:
        st.markdown("<h3 style='margin:4rem 0 1.5rem;'>Unlock Enterprise Remediation</h3>", unsafe_allow_html=True)
        st.link_button("SECURE ACCESS — $9 ONE-TIME", "https://porschza.gumroad.com/l/AEGIS",
                       type="primary", use_container_width=True)

        passcode = st.text_input("ENTER ACCESS PASSCODE", type="password")
        if st.button("UNLOCK FULL REPORT"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.error("ACCESS DENIED — Invalid passcode.")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("START NEW AUDIT SESSION", use_container_width=True):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div class='app-footer'>WAT SYSTEMS | AEGIS v32.0 — Supreme Logic Authority © 2026</div>", unsafe_allow_html=True)
