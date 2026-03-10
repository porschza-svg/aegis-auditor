import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. GEMINI NEURAL UI SYSTEM (AI PLUGIN STYLE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS AI | Gemini Extension",
    layout="centered", # เปลี่ยนเป็น Centered เพื่ออารมณ์ Chat/Plugin
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Persistence Control (System Logic Intact)
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The Gemini Design Framework (Aurora & Clean Obsidian)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Reset to Gemini Atmosphere */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { 
        background: radial-gradient(circle at top right, #1a1a2e 0%, #000000 50%, #000000 100%);
        color: #e0e0e0; 
        font-family: 'Inter', sans-serif; 
    }
    
    .block-container { padding-top: 4rem !important; max-width: 800px !important; }

    /* 1. Gemini Branding Header */
    .gemini-header {
        text-align: left;
        margin-bottom: 50px;
    }
    .gemini-logo {
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .gemini-sparkle { color: #8ab4f8; font-size: 1.2rem; vertical-align: super; margin-left: 5px; }
    .plugin-tag {
        font-size: 10px;
        font-weight: 600;
        color: #8b949e;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* 2. Neural Matrix Status */
    .status-row { display: flex; gap: 10px; margin-bottom: 30px; }
    .status-pill {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 8px 16px;
        border-radius: 100px;
        font-size: 11px;
        font-weight: 500;
        color: #8ab4f8;
    }

    /* 3. The Intelligence Intake (Gemini Input Style) */
    .stTextArea textarea { 
        background-color: #0d0d0d !important; 
        border: 1px solid #222 !important; 
        border-radius: 24px !important; 
        color: #f3f4f6 !important; 
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 25px !important;
        line-height: 1.6;
        min-height: 300px !important;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTextArea textarea:focus { border-color: #8ab4f8 !important; background: #111 !important; box-shadow: 0 0 20px rgba(66, 133, 244, 0.1) !important; }

    /* 4. Neural Execution Button */
    div.stButton > button {
        background: linear-gradient(90deg, #4285F4, #9B72CB) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 100px !important;
        padding: 12px 35px !important;
        width: auto !important;
        border: none !important;
        transition: 0.3s all;
        margin-top: 15px;
        box-shadow: 0 4px 15px rgba(66, 133, 244, 0.2);
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 8px 25px rgba(155, 114, 203, 0.3); }

    /* 5. The Reveal: Neural Dissection */
    .result-aura {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 28px;
        margin-top: 50px;
    }
    .score-label { font-size: 0.9rem; color: #8b949e; letter-spacing: 1px; margin-bottom: 10px; }
    .score-val { font-size: 6rem; font-weight: 700; color: #ffffff; line-height: 1; margin: 10px 0; letter-spacing: -3px; }
    .badge-ai { background: rgba(138, 180, 248, 0.1); color: #8ab4f8; padding: 4px 12px; border-radius: 100px; font-size: 11px; font-weight: 600; margin-top: 15px; display: inline-block; }

    /* 6. Finding Cards (Plugin Response Style) */
    .finding-block {
        border-top: 1px solid #222;
        padding: 30px 0;
        margin-top: 30px;
    }
    .f-header { display: flex; align-items: center; gap: 10px; color: #f28b82; font-size: 0.85rem; font-weight: 700; margin-bottom: 15px; }
    .f-title { font-size: 1.6rem; font-weight: 600; color: #ffffff; margin-bottom: 10px; line-height: 1.3; }
    .f-desc { font-size: 1.1rem; color: #bdc1c6; line-height: 1.7; }

    /* 7. Paywall: Restricted Intelligence */
    .paywall-box {
        background: #111;
        border: 1px dashed #333;
        padding: 40px;
        text-align: center;
        margin-top: 20px;
        border-radius: 20px;
    }
    .locked-label { font-size: 11px; font-weight: 700; color: #fdd663; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; display: block; }

    /* 8. Share authority on X */
    .share-btn { 
        display: inline-block; 
        color: #ffffff !important; 
        padding: 10px 25px; 
        border-radius: 100px; 
        text-decoration: none; 
        font-weight: 600; 
        font-size: 0.9rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #333;
        transition: 0.3s; 
    }
    .share-btn:hover { background: #fff; color: #000 !important; }

    .footer { text-align: center; color: #444; font-size: 0.8rem; margin-top: 8rem; padding-bottom: 3rem; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (SYSTEM LOGIC)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS NEURAL* | Score: {score}% | Issues: {issues_count} | 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (AUTO-ROUTING)
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
    <div class="gemini-header">
        <h1 class="gemini-logo">AEGIS Auditor <span class="gemini-sparkle">✦</span></h1>
        <div class="plugin-tag">Powered by WAT SYSTEMS | Universal Logic Authority</div>
    </div>
""", unsafe_allow_html=True)

# Neural Matrix Status
st.markdown("""
    <div class="status-row">
        <div class="status-pill">Code Security</div>
        <div class="status-pill">Workflow Logic</div>
        <div class="status-pill">Contract Audit</div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("", placeholder="How can AEGIS analyze your logic today? Paste architectural DNA...")

if st.button("Analyze Logic"):
    if not payload.strip(): st.error("Please provide data for analysis.")
    else:
        with st.spinner("Thinking..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (GEMINI EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>TRUST INDEX</div><div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div class='badge-ai'>Analysis Authenticated by AEGIS Neural Core</div>", unsafe_allow_html=True)
    
    # Plugin Viral Share
    share_msg = f"My project logic scored {score}% on AEGIS Auditor. Verified by WAT SYSTEMS 🛡️✦"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div style='margin-top:2.5rem; text-align:left;'><a href='{share_url}' target='_blank' class='share-btn'>Broadcast on 𝕏</a></div>", unsafe_allow_html=True)

    # Detailed Risks (High Quality Plugin Value)
    st.write("")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class="finding-block">
                <div class="f-header">Critical Vulnerability {i+1:02}</div>
                <div class="f-title">{f.get('issue')}</div>
                <div class="f-desc">{f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall for The Cure
        if not st.session_state.unlocked:
            st.markdown("""
                <div class="paywall-box">
                    <span class="locked-label">Remediation Encrypted</span>
                    <div style="color:#666; font-size:0.9rem;">Upgrade to Enterprise Pass to unlock technical solution.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**TECHNICAL SOLUTION:**")
            st.code(f.get('the_cure'), language='python')

    # Premium Global Conversion
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 Secure Enterprise Pass ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("Enter Passcode:", type="password")
        if st.button("Unlock All Remediation"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("Access Denied.")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Start New Scan", type="secondary"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div class='footer'>WAT SYSTEMS | AEGIS v36.0 | NEURAL AUTHORITY</div>", unsafe_allow_html=True)
