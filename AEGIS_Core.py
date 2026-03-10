import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. SOVEREIGN DESIGN SYSTEM (ULTRA-PREMIUM)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | UNIVERSAL AUTHORITY", 
    layout="wide", 
    page_icon="🛡️"
)

# Initialize States (Core Logic Unchanged)
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The Obsidian Enterprise Framework
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Reset & Authority Background */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { background-color: #000000; }
    
    .block-container { 
        padding-top: 5rem !important; 
        max-width: 1000px !important; 
    }

    /* Typography Authority */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif !important; 
        color: #ffffff; 
        -webkit-font-smoothing: antialiased;
    }

    /* Header: The Billion Dollar Signature */
    .brand-section {
        padding-bottom: 80px;
        text-align: left;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 60px;
    }
    .brand-logo {
        font-weight: 900;
        font-size: 5.5rem;
        letter-spacing: -6px;
        color: #ffffff;
        margin: 0;
        line-height: 0.75;
        background: linear-gradient(180deg, #FFFFFF 0%, #444444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-meta {
        font-size: 11px;
        font-weight: 700;
        color: #58a6ff;
        letter-spacing: 12px;
        text-transform: uppercase;
        margin-top: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .brand-meta::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, #58a6ff, transparent);
        opacity: 0.3;
    }

    /* Matrix Pillar Display (Stark Industrial) */
    .pillar-row {
        display: flex;
        gap: 1px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 50px;
    }
    .pillar-box {
        flex: 1;
        background: #000000;
        padding: 30px 25px;
        transition: 0.4s;
    }
    .pillar-box:hover { background: #050505; }
    .p-id { font-size: 8px; font-weight: 900; color: #444; text-transform: uppercase; letter-spacing: 2px; }
    .p-title { font-size: 12px; font-weight: 700; color: #ffffff; margin-top: 8px; letter-spacing: 1px; }

    /* The Obsidian Terminal */
    .stTextArea textarea { 
        background-color: #020202 !important; 
        border: 1px solid #111111 !important; 
        border-radius: 4px !important; 
        color: #ededed !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 16px !important;
        padding: 40px !important;
        line-height: 1.8;
        min-height: 400px !important;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5) !important;
    }
    .stTextArea textarea:focus { border-color: #333333 !important; }

    /* Action Trigger (Executioner Style) */
    div.stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        border-radius: 2px !important;
        padding: 28px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 6px !important;
        transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1);
        margin-top: 40px;
    }
    div.stButton > button:hover { 
        background: #58a6ff !important; 
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(88, 166, 255, 0.3);
    }

    /* Audit Result: The Reveal Wall */
    .result-wall {
        border: 1px solid #111111;
        padding: 100px 80px;
        margin-top: 100px;
        background: #000000;
        position: relative;
    }
    .result-wall::before {
        content: ""; position: absolute; top: -1px; left: -1px; width: 80px; height: 80px;
        border-top: 2px solid #58a6ff; border-left: 2px solid #58a6ff;
    }
    .score-label { font-size: 13px; font-weight: 800; color: #58a6ff; letter-spacing: 6px; text-transform: uppercase; }
    .score-hero { font-size: 180px; font-weight: 900; color: #ffffff; letter-spacing: -18px; line-height: 0.8; margin: 40px 0; }
    
    /* Detailed Finding Cards (High-End Audit) */
    .finding-block {
        border-top: 1px solid #111111;
        padding: 60px 0;
        margin-top: 60px;
    }
    .f-id { font-size: 10px; font-weight: 900; color: #ff4d4d; text-transform: uppercase; letter-spacing: 3px; }
    .f-title { font-size: 28px; font-weight: 700; color: #ffffff; margin: 15px 0; letter-spacing: -0.5px; }
    .f-impact { font-size: 18px; color: #888888; line-height: 1.8; font-weight: 400; }

    /* The Cure: Exclusive Chamber */
    .cure-chamber {
        background: #050505;
        border: 1px solid #221d00;
        padding: 60px;
        text-align: center;
        margin-top: 40px;
    }
    .locked-tag { font-size: 11px; font-weight: 800; color: #e3b341; letter-spacing: 6px; text-transform: uppercase; display: block; margin-bottom: 25px; }

    /* Viral Share Integration */
    .share-strip {
        margin-top: 100px;
        padding-top: 60px;
        border-top: 1px solid #111111;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .share-text { font-size: 13px; color: #555; font-weight: 600; letter-spacing: 1px; }
    .share-link { 
        font-size: 14px; font-weight: 800; color: #ffffff; text-decoration: none; 
        border-bottom: 2px solid #58a6ff; padding-bottom: 8px; transition: 0.3s;
    }
    .share-link:hover { color: #58a6ff; transform: translateX(5px); }
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

# Industrial Module Grid
st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-box'><span class='p-id'>PROTOCOL_01</span><div class='p-title'>CODE_SECURITY</div></div>
        <div class='pillar-box'><span class='p-id'>PROTOCOL_02</span><div class='p-title'>LOGIC_FLOW</div></div>
        <div class='pillar-box'><span class='p-id'>PROTOCOL_03</span><div class='p-title'>WEB3_AUDIT</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("PAYLOAD_INJECTION:", height=400, placeholder="/// INJECT ARCHITECTURAL DNA FOR DISSECTION")

if st.button("EXECUTE SUPREME AUDIT"):
    if not payload.strip(): st.error("ERROR: NULL_PAYLOAD")
    else:
        with st.spinner("Decoding DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. AUDIT REVEAL (PREMIUM FREEMIUM EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-wall'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL_LOGIC_INTEGRITY</div><div class='score-hero'>{score}%</div>", unsafe_allow_html=True)
    
    # Premium Social Share
    share_msg = f"My project logic scored {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"""
        <div class='share-strip'>
            <span class='share-text'>PUBLIC_AUTHORITY_VERIFIED</span>
            <a href='{share_url}' target='_blank' class='share-link'>𝕏 BROADCAST AUTHORITY</a>
        </div>
    """, unsafe_allow_html=True)

    # Detailed Risks (High Quality Freemium Value)
    st.write("")
    st.subheader("🚨 DETECTED LOGIC FAILURES")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class='finding-block'>
                <span class='f-id'>RISK_IDENTIFIER_{i+1:02}</span>
                <div class='f-title'>{f.get('issue')}</div>
                <div class='f-impact'><b>ANALYSIS:</b> "{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall for The Cure
        if not st.session_state.unlocked:
            st.markdown("<div class='cure-chamber'><span class='locked-tag'>🔒 REMEDIATION_RESTRICTED</span></div>", unsafe_allow_html=True)
        else:
            st.success("**TECHNICAL REMEDIATION:**")
            st.code(f.get('the_cure'), language='python')

    # Premium Conversion Experience
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 SECURE SOVEREIGN PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("ENTER_PASSCODE:", type="password")
        if st.button("UNLOCK_REMEDIATION"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS_DENIED")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("RESET_AUDIT_TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#1a1a1a; font-size:10px; margin-top:250px; font-weight:700; letter-spacing:10px;'>WAT SYSTEMS | AEGIS v33.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
