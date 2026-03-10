import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. ABSOLUTE SOVEREIGN DESIGN SYSTEM (Billion Dollar Vision)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | UNIVERSAL AUTHORITY", 
    layout="wide", # ใช้ Wide เพื่อคุม Spacing เองทั้งหมด
    page_icon="🛡️"
)

# Initialize States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "WAT" Proprietary Enterprise UI Framework
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=JetBrains+Mono:wght@500&display=swap');

    /* 1. Root Layout Neutralization */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { background-color: #000000; }
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 900px !important; 
        background-color: #000000;
    }
    
    /* 2. Global Typography Authority */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif !important; 
        color: #ffffff; 
    }

    /* 3. Sovereign Brand Identity */
    .brand-section {
        padding: 120px 0 80px 0;
        text-align: left;
        border-bottom: 1px solid #111111;
        margin-bottom: 60px;
    }
    .brand-logo {
        font-weight: 900;
        font-size: 5rem;
        letter-spacing: -5px;
        color: #ffffff;
        margin: 0;
        line-height: 0.8;
        background: linear-gradient(180deg, #FFFFFF 0%, #333333 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-meta {
        font-size: 11px;
        font-weight: 700;
        color: #58a6ff;
        letter-spacing: 10px;
        text-transform: uppercase;
        margin-top: 25px;
        opacity: 0.8;
    }

    /* 4. Industrial Intelligence Matrix */
    .matrix-row {
        display: flex;
        gap: 20px;
        margin-bottom: 40px;
    }
    .matrix-item {
        flex: 1;
        background: #000000;
        border: 1px solid #161616;
        padding: 30px;
        position: relative;
        transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .matrix-item:hover { border-color: #333333; transform: translateY(-2px); }
    .m-label { font-size: 9px; font-weight: 800; color: #444; text-transform: uppercase; letter-spacing: 2px; }
    .m-status { font-size: 13px; font-weight: 700; color: #ffffff; margin-top: 8px; display: block; }

    /* 5. Terminal Execution Area */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #161616 !important; 
        border-radius: 0px !important; 
        color: #ededed !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 16px !important;
        padding: 40px !important;
        line-height: 1.8;
        min-height: 400px !important;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; background-color: #050505 !important; }

    /* 6. Billion-Dollar CTA */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 14px !important;
        border-radius: 0px !important;
        padding: 30px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 6px !important;
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        margin-top: 40px;
    }
    div.stButton > button:hover { 
        background-color: #58a6ff !important; 
        color: #ffffff !important;
        box-shadow: 0 20px 60px rgba(88, 166, 255, 0.2);
    }

    /* 7. Audit Result: The Reveal */
    .result-wall {
        background: #000000;
        border: 1px solid #161616;
        padding: 100px 80px;
        margin-top: 120px;
        position: relative;
    }
    .result-wall::before {
        content: "";
        position: absolute;
        top: -1px; left: -1px; width: 100px; height: 100px;
        border-top: 2px solid #58a6ff; border-left: 2px solid #58a6ff;
    }
    .score-tag { font-size: 13px; font-weight: 800; color: #58a6ff; letter-spacing: 6px; text-transform: uppercase; }
    .score-hero { font-size: 180px; font-weight: 900; color: #ffffff; letter-spacing: -15px; line-height: 0.9; margin: 40px 0; }
    
    /* 8. Risk Disclosure (Freemium Value) */
    .risk-block {
        border-top: 1px solid #111;
        padding: 60px 0;
        margin-top: 60px;
    }
    .risk-id { font-size: 11px; font-weight: 900; color: #ff4d4d; text-transform: uppercase; letter-spacing: 2px; }
    .risk-title { font-size: 28px; font-weight: 700; color: #ffffff; margin: 15px 0; }
    .risk-impact { font-size: 18px; color: #777777; line-height: 1.7; font-weight: 400; }

    /* 9. The Cure: Premium Path */
    .cure-chamber {
        background: #050505;
        border: 1px solid #221d00;
        padding: 60px;
        text-align: center;
        margin-top: 40px;
    }
    .cure-label { font-size: 10px; font-weight: 800; color: #e3b341; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 20px; display: block; }

    /* 10. Social Logic (Share on X) */
    .share-container { margin-top: 80px; text-align: left; }
    .share-link { 
        font-size: 14px; 
        font-weight: 700; 
        color: #ffffff; 
        text-decoration: none; 
        border-bottom: 1px solid #ffffff; 
        padding-bottom: 5px;
        transition: 0.3s;
    }
    .share-link:hover { color: #58a6ff; border-color: #58a6ff; }
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
    <div class='brand-section'>
        <h1 class='brand-logo'>AEGIS</h1>
        <div class='brand-meta'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# The Matrix Grid
st.markdown("""
    <div class='matrix-row'>
        <div class='matrix-item'><span class='m-label'>L-PROTOCOL</span><span class='m-status'>CODE ENFORCEMENT</span></div>
        <div class='matrix-item'><span class='m-label'>L-STATUS</span><span class='m-status'>CORE_ACTIVE</span></div>
        <div class='matrix-item'><span class='m-label'>L-REGION</span><span class='m-status'>GLOBAL_UPLINK</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("PAYLOAD_UPLINK:", placeholder="/// INJECT ARCHITECTURAL DNA FOR DISSECTION")

if st.button("EXECUTE SUPREME AUDIT"):
    if not payload.strip(): st.error("ERROR: NULL_PAYLOAD")
    else:
        with st.spinner("Decoding DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. AUDIT REVEAL (THE AUTHORITY REVEAL)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-wall'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-tag'>GLOBAL_TRUST_SCORE</div><div class='score-hero'>{score}%</div>", unsafe_allow_html=True)
    
    # Viral Loop Integration
    share_msg = f"My project logic scored {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div class='share-container'><a href='{share_url}' target='_blank' class='share-link'>𝕏 BROADCAST AUTHORITY RESULT</a></div>", unsafe_allow_html=True)

    # Detailed Risks (High Quality Freemium)
    st.write("")
    st.subheader("🚨 STRUCTURAL DEVIATIONS DETECTED")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class='risk-block'>
                <span class='risk-id'>RISK_IDENTIFIER_{i+1:02}</span>
                <div class='risk-title'>{f.get('issue')}</div>
                <div class='risk-impact'><b>ANALYSIS:</b> "{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall: The Cure
        if not st.session_state.unlocked:
            st.markdown("<div class='cure-chamber'><span class='cure-label'>🔒 REMEDIATION_RESTRICTED</span></div>", unsafe_allow_html=True)
        else:
            st.success("**TECHNICAL SOLUTION:**")
            st.code(f.get('the_cure'), language='python')

    # Premium Global Conversion
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 SECURE SOVEREIGN PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("PASSCODE_ENTRY:", type="password")
        if st.button("UNLOCK_REMEDIATION"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS_DENIED")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("RESET_TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#1a1a1a; font-size:10px; margin-top:200px; font-weight:700; letter-spacing:8px;'>WAT SYSTEMS | AEGIS v32.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
