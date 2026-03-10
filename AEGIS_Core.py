import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. ARCHITECTURAL UI SYSTEM (UNICORN GRADE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | AUTHORITY", 
    layout="wide", 
    page_icon="🛡️"
)

# Persistence Control (Logic Unchanged)
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "Sovereign" Design Framework
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* 1. Global Decimation of Streamlit Default Look */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { background-color: #000000; }
    .block-container { 
        padding-top: 3rem !important; 
        max-width: 1200px !important; 
        background-color: #000000;
    }
    
    /* 2. Global Typography Enforcer */
    html, body, [class*="css"] { 
        font-family: 'Space Grotesk', sans-serif !important; 
        color: #ffffff; 
    }

    /* 3. The Billion Dollar Hero Section */
    .hero-section {
        padding: 100px 0 60px 0;
        text-align: left;
        border-bottom: 1px solid #111111;
        margin-bottom: 80px;
    }
    .brand-id {
        font-weight: 700;
        font-size: 6rem;
        letter-spacing: -6px;
        color: #ffffff;
        margin: 0;
        line-height: 0.8;
        display: inline-block;
    }
    .brand-meta {
        font-size: 12px;
        font-weight: 500;
        color: #00f0ff;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-top: 25px;
        opacity: 0.9;
    }

    /* 4. Industrial Protocol Matrix */
    .protocol-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2px;
        background: #111;
        border: 1px solid #111;
        margin-bottom: 60px;
    }
    .protocol-box {
        background: #000;
        padding: 40px;
        transition: 0.3s;
    }
    .protocol-box:hover { background: #050505; }
    .p-label { font-size: 10px; font-weight: 700; color: #444; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; display: block; }
    .p-value { font-size: 14px; font-weight: 400; color: #fff; letter-spacing: 1px; }

    /* 5. The Intelligence Intake (Terminal) */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #111 !important; 
        border-radius: 0px !important; 
        color: #00f0ff !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 16px !important;
        padding: 50px !important;
        line-height: 1.8;
        min-height: 450px !important;
        box-shadow: inset 0 0 50px rgba(0,0,0,1) !important;
    }
    .stTextArea textarea:focus { border-color: #00f0ff !important; box-shadow: none !important; }

    /* 6. Execution Catalyst (Primary Button) */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 0px !important;
        padding: 35px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 10px !important;
        transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        margin-top: 50px;
    }
    div.stButton > button:hover { 
        background-color: #00f0ff !important; 
        color: #000 !important;
        transform: translateY(-5px);
        box-shadow: 0 30px 60px rgba(0, 240, 255, 0.2);
    }

    /* 7. The Reveal: Logic Integrity Wall */
    .reveal-wall {
        border-top: 1px solid #111;
        padding: 120px 0;
        margin-top: 150px;
    }
    .score-indicator { font-size: 14px; font-weight: 600; color: #444; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 40px; }
    .score-giant { font-size: 240px; font-weight: 700; color: #ffffff; letter-spacing: -22px; line-height: 0.75; margin: 0; }
    
    /* 8. Risk Dissection (High-Quality Audit) */
    .finding-entry {
        border-bottom: 1px solid #111;
        padding: 80px 0;
    }
    .entry-meta { font-size: 11px; font-weight: 700; color: #ff003c; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 25px; display: block; }
    .entry-title { font-size: 42px; font-weight: 500; color: #ffffff; margin-bottom: 25px; letter-spacing: -1.5px; line-height: 1.1; }
    .entry-impact { font-size: 20px; color: #666; line-height: 1.7; font-weight: 300; }

    /* 9. The Cure Chamber: Restricted Path */
    .cure-gate {
        background: #030303;
        border: 1px solid #1a1a1a;
        padding: 100px 50px;
        text-align: center;
        margin-top: 60px;
    }
    .gate-label { font-size: 12px; font-weight: 700; color: #00f0ff; letter-spacing: 6px; text-transform: uppercase; display: block; margin-bottom: 30px; }

    /* 10. Social Logic (Share on X) */
    .share-block { margin-top: 120px; text-align: right; }
    .share-link { 
        font-size: 16px; 
        font-weight: 700; 
        color: #ffffff; 
        text-decoration: none; 
        padding: 15px 40px;
        border: 1px solid #222;
        transition: 0.3s;
    }
    .share-link:hover { border-color: #00f0ff; color: #00f0ff; }
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
            msg = f"🛡️ *[AEGIS AUTHORITY]*\n\n● *Status:* {status}\n● *Score:* {score}%\n● *Findings:* {issues_count}\n\n📡 _WAT SYSTEMS_"
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
    <div class='hero-section'>
        <h1 class='brand-id'>AEGIS</h1>
        <div class='brand-meta'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# High-Detail Protocol Matrix
st.markdown("""
    <div class='protocol-grid'>
        <div class='protocol-box'><span class='p-label'>L-PROTOCOL</span><div class='p-value'>LOGIC_ENFORCEMENT</div></div>
        <div class='protocol-box'><span class='p-label'>L-STATUS</span><div class='p-value'>SYSTEM_OPERATIONAL</div></div>
        <div class='protocol-box'><span class='p-label'>L-AUTHORITY</span><div class='p-value'>WAT_SYSTEMS_GLOBAL</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("PAYLOAD_INJECTION:", placeholder="/// INJECT ARCHITECTURAL DNA FOR DISSECTION")

if st.button("EXECUTE SUPREME AUDIT"):
    if not payload.strip(): st.error("ERROR: NULL_PAYLOAD")
    else:
        with st.spinner("Processing structural integrity..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. AUDIT REVEAL (PREMIUM AUTHORITY EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='reveal-wall'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-indicator'>LOGIC_INTEGRITY_INDEX</div><div class='score-giant'>{score}%</div>", unsafe_allow_html=True)
    
    # Premium Viral Integration
    share_msg = f"Logic Authority Scanned: {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div class='share-block'><a href='{share_url}' target='_blank' class='share-link'>𝕏 BROADCAST AUTHORITY RESULT</a></div>", unsafe_allow_html=True)

    # Detailed Risks (True Freemium Value)
    st.write("")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class='finding-entry'>
                <span class='entry-meta'>VULNERABILITY_ID_{i+1:02}</span>
                <div class='entry-title'>{f.get('issue')}</div>
                <div class='entry-impact'>{f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # The Cure Path
        if not st.session_state.unlocked:
            st.markdown("<div class='cure-gate'><span class='gate-label'>🔒 REMEDIATION_RESTRICTED_ACCESS</span></div>", unsafe_allow_html=True)
        else:
            st.success("**TECHNICAL_REMEDIATION_LOG:**")
            st.code(f.get('the_cure'), language='python')

    # Premium Global Conversion
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 SECURE SOVEREIGN ENTERPRISE PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("PASSCODE_AUTHORIZATION:", type="password")
        if st.button("UNLOCK_REMEDIATION"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS_DENIED")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("RESET_TERMINAL_SESSION"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#111; font-size:12px; margin-top:250px; font-weight:700; letter-spacing:15px;'>WAT SYSTEMS | AEGIS v34.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
