import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. VANGUARD ENTERPRISE UI SYSTEM (UNICORN GRADE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | VANGUARD AUTHORITY",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Persistence Control (Core Logic Untouched)
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "Vanguard" Design Framework
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Reset & Authority Dark */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { background-color: #000000; color: #ffffff; }
    .block-container { 
        padding-top: 5rem !important; 
        max-width: 1200px !important; 
        background-color: #000000;
    }
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif !important; 
    }

    /* 1. Monolith Header Section */
    .header-container {
        padding: 100px 0 60px 0;
        text-align: center;
    }
    .logo-hero {
        font-size: 10rem;
        font-weight: 900;
        letter-spacing: -0.08em;
        color: #ffffff;
        line-height: 0.8;
        margin: 0;
        text-shadow: 0 0 80px rgba(255, 255, 255, 0.1);
    }
    .subtitle-hero {
        font-size: 1rem;
        font-weight: 400;
        color: #6b7280;
        letter-spacing: 0.6em;
        text-transform: uppercase;
        margin-top: 2rem;
    }

    /* 2. Operational Status Matrix */
    .matrix-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 4rem 0;
    }
    .matrix-card {
        background: #050505;
        border: 1px solid #1a1a1a;
        padding: 2rem 3rem;
        border-radius: 0px;
        text-align: center;
        transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        min-width: 250px;
    }
    .matrix-card:hover { border-color: #3b82f6; box-shadow: 0 0 40px rgba(59,130,246,0.1); }
    .m-status { font-size: 0.8rem; color: #10b981; font-weight: 700; letter-spacing: 0.2em; display: block; margin-bottom: 0.5rem; }
    .m-label { font-size: 1.1rem; font-weight: 600; color: #ffffff; }

    /* 3. The Obsidian Terminal */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 0px !important; 
        color: #3b82f6 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.1rem !important;
        padding: 40px !important;
        line-height: 1.8;
        min-height: 480px !important;
        box-shadow: inset 0 0 50px rgba(0,0,0,1) !important;
    }
    .stTextArea textarea:focus { border-color: #3b82f6 !important; }

    /* 4. Execution Catalyst (Modern Pill) */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 9999px !important;
        padding: 1.2rem 4rem !important;
        width: auto !important;
        min-width: 280px;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 5px !important;
        transition: 0.4s all;
        margin: 2rem auto;
        display: block;
    }
    div.stButton > button:hover { 
        background-color: #3b82f6 !important; 
        color: white !important;
        transform: translateY(-4px);
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.3);
    }

    /* 5. The Reveal: Authority Wall */
    .result-wall {
        border-top: 1px solid #1a1a1a;
        padding: 100px 0;
        margin-top: 100px;
        text-align: center;
    }
    .score-label { font-size: 1.1rem; font-weight: 600; color: #4b5563; letter-spacing: 0.4em; margin-bottom: 2rem; }
    .score-hero { font-size: 14rem; font-weight: 900; color: #ffffff; letter-spacing: -0.06em; line-height: 0.9; margin: 0; }
    
    /* 6. Risk Dissection (High-End Audit) */
    .finding-box {
        background: #030303;
        border: 1px solid #111;
        border-left: 4px solid #ef4444;
        padding: 4rem;
        margin-top: 3rem;
        text-align: left;
        transition: 0.3s;
    }
    .f-tag { font-size: 0.9rem; color: #ef4444; font-weight: 700; letter-spacing: 0.2em; display: block; margin-bottom: 1.5rem; }
    .f-title { font-size: 2.8rem; font-weight: 700; color: #ffffff; margin-bottom: 1.5rem; line-height: 1.1; }
    .f-impact { font-size: 1.3rem; color: #6b7280; line-height: 1.8; font-weight: 400; }

    /* 7. The Cure: Restricted Access */
    .paywall-gate {
        background: #080808;
        border: 1px solid #1f1f1f;
        padding: 5rem 3rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 1rem;
    }
    .paywall-tag { font-size: 1rem; font-weight: 700; color: #f59e0b; letter-spacing: 0.3em; text-transform: uppercase; margin-bottom: 2rem; display: block; }

    /* 8. Share authority on X */
    .share-btn { 
        display: inline-block; 
        background: transparent; 
        border: 1px solid #374151; 
        color: #ffffff !important; 
        padding: 1rem 3rem; 
        border-radius: 9999px; 
        text-decoration: none; 
        font-weight: 600; 
        font-size: 1rem;
        transition: 0.3s; 
    }
    .share-btn:hover { background: #ffffff; color: #000 !important; }

    /* Footer */
    .footer { text-align: center; color: #374151; font-size: 1rem; margin-top: 10rem; padding-bottom: 5rem; letter-spacing: 0.1em; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (SYSTEM LOGIC PRESERVED)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS AUTHORITY* | Score: {score}% | Issues: {issues_count} | 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (SYSTEM LOGIC PRESERVED)
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
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class="header-container">
        <h1 class="logo-hero">AEGIS</h1>
        <div class="subtitle-hero">UNIVERSAL LOGIC AUTHORITY — WAT SYSTEMS</div>
    </div>
""", unsafe_allow_html=True)

# Operational Status Matrix
st.markdown("""
    <div class="matrix-container">
        <div class="matrix-card"><span class="m-status">OPERATIONAL</span><div class="m-label">CODE SECURITY</div></div>
        <div class="matrix-card"><span class="m-status">OPERATIONAL</span><div class="m-label">BUSINESS LOGIC</div></div>
        <div class="matrix-card"><span class="m-status">OPERATIONAL</span><div class="m-label">SMART CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("", placeholder="/// INJECT LOGIC DNA FOR AUTHORITATIVE DISSECTION")

# Layout สำหรับปุ่ม Execute
_, col_btn, _ = st.columns([1, 1.5, 1])
with col_btn:
    if st.button("EXECUTE AUDIT"):
        if not payload.strip(): st.error("ERROR: NULL_PAYLOAD")
        else:
            with st.spinner("Decoding DNA..."):
                st.session_state.result = run_audit(payload)
                st.session_state.scanned = True
                st.session_state.unlocked = False
                st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (VANGUARD EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-wall'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL_LOGIC_INTEGRITY</div><div class='score-hero'>{score}</div>", unsafe_allow_html=True)
    
    # Premium Viral Share
    share_msg = f"My project logic scored {score}% on AEGIS. Verified by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div style='margin-top:4rem;'><a href='{share_url}' target='_blank' class='share-btn'>𝕏 BROADCAST AUTHORITY RESULT</a></div>", unsafe_allow_html=True)

    # Detailed Risks (High-Fidelity Freemium)
    st.write("")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class="finding-box">
                <span class="f-tag">RISK_IDENTIFIER_{i+1:02}</span>
                <div class="f-title">{f.get('issue')}</div>
                <div class="f-impact"><b>IMPACT ANALYSIS:</b> "{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall for The Cure
        if not st.session_state.unlocked:
            st.markdown("""
                <div class="paywall-gate">
                    <span class="paywall-tag">🔒 REMEDIATION_LOCKED</span>
                    <div style="color:#4b5563; margin-bottom:2rem;">SECURE ENTERPRISE PASS TO DEPLOY TECHNICAL SOLUTION.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**TECHNICAL_REMEDIATION_LOG:**")
            st.code(f.get('the_cure'), language='python')

    # Premium Global Conversion
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 SECURE ENTERPRISE PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("ENTER_PASSCODE:", type="password")
        if st.button("UNLOCK_REMEDIATION"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS_DENIED")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("START NEW SESSION", type="secondary"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div class='footer'>WAT SYSTEMS | AEGIS v35.0 | VANGUARD AUTHORITY</div>", unsafe_allow_html=True)
