import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI SYSTEM (INDUSTRIAL PREMIUM)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | WAT SYSTEMS", 
    layout="centered", 
    page_icon="🛡️"
)

# Initialize Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# Premium Industrial CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@500&display=swap');
    
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    
    /* Sovereign Brand Header */
    .header-box { border-left: 5px solid #58a6ff; padding-left: 25px; margin: 50px 0; }
    .logo-text { font-weight: 900; font-size: 2.8rem; letter-spacing: -2px; color: #ffffff; margin: 0; line-height: 1; }
    .motto-text { font-size: 10px; font-weight: 700; color: #8b949e; letter-spacing: 5px; text-transform: uppercase; margin-top: 5px; }

    /* Matrix Pillar Display */
    .pillar-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 40px; }
    .pillar-card { background: #161b22; border: 1px solid #30363d; padding: 18px; border-radius: 8px; text-align: center; border-bottom: 3px solid #30363d; }
    .pillar-tag { font-size: 8px; font-weight: 900; color: #58a6ff; text-transform: uppercase; margin-bottom: 4px; display: block; }
    .pillar-name { font-size: 12px; font-weight: 700; color: #f0f6fc; }

    /* Industrial Terminal */
    .stTextArea textarea { 
        background-color: #010409 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 12px !important; 
        color: #e6edf3 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 25px !important;
        line-height: 1.6;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; box-shadow: 0 0 15px rgba(88, 166, 255, 0.1) !important; }

    /* Supreme Action Button */
    div.stButton > button {
        background: #238636 !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        padding: 22px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        transition: 0.2s all ease;
    }
    div.stButton > button:hover { background: #2ea043 !important; transform: translateY(-2px); box-shadow: 0 10px 30px rgba(35,134,54,0.3); }

    /* Result Architecture */
    .result-container { background: #0d1117; border: 1px solid #30363d; border-radius: 16px; padding: 50px; margin-top: 50px; box-shadow: 0 40px 80px rgba(0,0,0,0.6); }
    .score-label { font-size: 12px; font-weight: 800; color: #8b949e; letter-spacing: 4px; }
    .score-value { font-size: 100px; font-weight: 900; color: #ffffff; line-height: 1; margin: 15px 0; letter-spacing: -5px; }
    
    .alert-frame { background: rgba(248, 81, 73, 0.05); border: 1px solid rgba(248, 81, 73, 0.2); border-left: 6px solid #f85149; padding: 35px; border-radius: 4px; margin-top: 35px; }
    .alert-issue { color: #f85149; font-weight: 900; font-size: 20px; text-transform: uppercase; margin-bottom: 15px; }
    .alert-desc { font-size: 17px; font-weight: 400; color: #e6edf3; line-height: 1.6; }

    .paywall-box { background: #161b22; border: 1px solid #e3b341; padding: 40px; border-radius: 12px; text-align: center; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR SYSTEM (RE-ENGINEERED)
# ────────────────────────────────────────────────
def broadcast_to_telegram(score, status_text, flaw_name):
    try:
        # ใช้ชื่อที่สื่อความหมายชัดเจนใน Secrets
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
        
        if token and chat_id:
            icon = "🛡️" if score > 70 else "🚨"
            if "ERROR" in status_text: icon = "⚠️"
            
            message = (
                f"{icon} *[AEGIS AUTHORITY RADAR]*\n\n"
                f"● *STATUS:* {status_text}\n"
                f"● *SCORE:* {score}%\n"
                f"● *L-FLAW:* {flaw_name}\n\n"
                f"📡 _Uplink established by WAT SYSTEMS_"
            )
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=8)
    except Exception as e:
        st.sidebar.warning(f"Radar Link Suspended: {e}")

# ────────────────────────────────────────────────
# 3. SUPREME LOGIC ENGINE (PRECISION CONNECT)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        # Architect: เปลี่ยนชื่อ Secret ให้ตรงกับบริการที่ใช้จริง
        api_key = st.secrets.get("OPENROUTER_API_KEY", "")
        if not api_key: raise Exception("SECRET_FAILURE: 'OPENROUTER_API_KEY' NOT FOUND IN SETTINGS")
        
        # เลือก Model ฟรีที่เสถียรที่สุด (Google Gemini 1.5 Flash - Very High Availability)
        target_model = "google/gemini-flash-1.5"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://aegis.watsystems.tech", # Placeholder
            "X-Title": "AEGIS v14.0",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": target_model,
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        "You are AEGIS, the supreme Logic Auditor by WAT SYSTEMS. "
                        "Identify the single most critical logic flaw. Be factual, cold, and professional. "
                        "Output ONLY a valid JSON object: "
                        "{\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                    )
                },
                {"role": "user", "content": f"PAYLOAD_ANALYSIS_REQUEST:\n{payload[:15000]}"}
            ],
            "temperature": 0.0
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=50)
        
        if response.status_code != 200:
            err = response.json().get("error", {}).get("message", "Uplink Denied")
            raise Exception(f"OPENROUTER_REJECTION: {err}")
            
        result = response.json()
        if "choices" not in result: raise Exception("INVALID_RESPONSE_DATA")
            
        content = result['choices'][0]['message']['content'].strip()
        
        # Robust JSON extraction
        if "{" in content and "}" in content:
            content = content[content.find("{"):content.rfind("}")+1]
            
        return json.loads(content)
        
    except Exception as e:
        broadcast_to_telegram(0, f"ERROR: {str(e)[:50]}", "UPLINK_FAILURE")
        return {
            "trust_score": 0, 
            "findings": [{
                "issue": "CORE UPLINK SEVERED", 
                "catastrophic_impact": str(e), 
                "the_cure": "Ensure 'OPENROUTER_API_KEY' is valid and credit is available."
            }]
        }

# ────────────────────────────────────────────────
# 4. SYSTEM INTERFACE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='header-box'>
        <div class='logo-text'>AEGIS</div>
        <div class='motto-text'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='pillar-grid'>
        <div class='pillar-card'><span class='pillar-tag'>AUDIT P-01</span><span class='pillar-name'>CODE SECURITY</span></div>
        <div class='pillar-card'><span class='pillar-tag'>AUDIT P-02</span><span class='pillar-name'>WORKFLOW</span></div>
        <div class='pillar-card'><span class='pillar-tag'>AUDIT P-03</span><span class='pillar-name'>SMART CONTRACTS</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD FOR DISSECTION:", height=320, placeholder="Paste architectural logic or source code for authoritative audit...")

if st.button("EXECUTE SUPREME AUDIT"):
    if not payload.strip():
        st.error("ERROR: SYSTEM REQUIRES DATA PAYLOAD.")
    else:
        with st.spinner("Processing structural integrity..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            
            # Successful Radar Broadcast
            if st.session_state.result and st.session_state.result.get('trust_score', 0) > 0:
                score = st.session_state.result.get('trust_score')
                issue = st.session_state.result.get('findings', [{}])[0].get('issue', 'Unknown')
                broadcast_to_telegram(score, "AUDIT_SUCCESS", issue)
                
            st.rerun()

# ────────────────────────────────────────────────
# 5. AUDIT REVEAL
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-value'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#58a6ff; color:#0d1117; display:inline-block; padding:3px 12px; border-radius:4px; font-size:11px; font-weight:900; letter-spacing:1px;'>VALIDATED BY AEGIS CORE</div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='alert-frame'>
                <div class='alert-issue'>● FATAL FLAW: {f.get('issue')}</div>
                <div style='color: #8b949e; font-size: 11px; font-weight: 800; margin-bottom: 8px; text-transform: uppercase;'>Catastrophic Impact:</div>
                <div class='alert-desc'>"{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.link_button("BROADCAST RESULTS ON X", f"https://twitter.com/intent/tweet?text=Logic Authority Scanned. Score: {score}%. 🛡️ Verified by WAT SYSTEMS.", use_container_width=True)

        # Sovereign Paywall
        st.write("")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='paywall-box'>
                    <div style='color:#e3b341; font-weight:900; font-size:11px; letter-spacing:3px; margin-bottom:12px;'>REMEDIATION ENCRYPTED</div>
                    <div style='color:#8b949e; font-size:13px; margin-bottom:20px;'>Remediation code is restricted to Sovereign Enterprise holders.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE SOVEREIGN PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            passcode = st.text_input("ACCESS PASSCODE:", type="password")
            if st.button("DECRYPT TECHNICAL SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("ACCESS DENIED.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.markdown("### 🟢 TECHNICAL SOLUTION")
            st.code(f.get('the_cure'), language='python')

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#30363d; font-size:10px; margin-top:100px; font-weight:700; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v14.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
