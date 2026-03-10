import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI ARCHITECTURE (PREMIUM MINIMALISM)
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

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    
    /* Sovereign Header */
    .header-container { text-align: left; border-left: 4px solid #58a6ff; padding-left: 20px; margin: 40px 0; }
    .brand-name { font-weight: 900; font-size: 2.5rem; letter-spacing: -1.5px; color: #ffffff; margin: 0; }
    .brand-motto { font-size: 10px; font-weight: 700; color: #8b949e; letter-spacing: 5px; text-transform: uppercase; }

    /* Matrix Status Indicators */
    .pillar-row { display: flex; gap: 15px; margin-bottom: 30px; }
    .pillar-item { flex: 1; background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; text-align: center; border-bottom: 3px solid #30363d; }
    .pillar-id { font-size: 9px; font-weight: 800; color: #58a6ff; display: block; margin-bottom: 4px; }
    .pillar-name { font-size: 12px; font-weight: 600; color: #f0f6fc; }

    /* Premium Terminal */
    .stTextArea textarea { 
        background-color: #010409 !important; 
        border: 2px solid #30363d !important; 
        border-radius: 12px !important; 
        color: #e6edf3 !important; 
        font-family: 'SF Mono', 'Fira Code', monospace !important;
        font-size: 15px !important;
        padding: 25px !important;
        line-height: 1.6;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; }

    /* Action Button: The Sovereign Green */
    div.stButton > button {
        background: #238636 !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        padding: 20px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        transition: 0.3s all cubic-bezier(0.4, 0, 0.2, 1);
    }
    div.stButton > button:hover { background: #2ea043 !important; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(35,134,54,0.4); }

    /* Result Aesthetics */
    .result-card { background: #0d1117; border: 1px solid #30363d; border-radius: 16px; padding: 50px; margin-top: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.5); }
    .score-label { font-size: 12px; font-weight: 800; color: #8b949e; letter-spacing: 3px; }
    .score-value { font-size: 96px; font-weight: 900; color: #ffffff; line-height: 1; margin: 15px 0; letter-spacing: -4px; }
    
    .alert-box { background: rgba(248, 81, 73, 0.08); border: 1px solid rgba(248, 81, 73, 0.2); border-left: 6px solid #f85149; padding: 30px; border-radius: 4px; margin-top: 30px; }
    .alert-title { color: #f85149; font-weight: 900; font-size: 14px; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 1px; }
    .alert-body { font-size: 18px; font-weight: 600; color: #f0f6fc; line-height: 1.5; }

    .paywall-container { background: #161b22; border: 1px solid #e3b341; padding: 40px; border-radius: 12px; text-align: center; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (NOTIFICATIONS)
# ────────────────────────────────────────────────
def send_telegram_alert(score, issue, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
        if token and chat_id:
            icon = "🚨" if status == "SUCCESS" else "⚠️"
            message = (
                f"{icon} *[AEGIS RADAR ALERT]*\n\n"
                f"● *Status:* {status}\n"
                f"● *Logic Score:* {score}%\n"
                f"● *Primary Flaw:* {issue}\n\n"
                f"🛡️ _Authenticated by WAT SYSTEMS_"
            )
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        st.sidebar.error(f"Telegram Link Failed: {e}")

# ────────────────────────────────────────────────
# 3. SUPREME AUDIT ENGINE (VERIFIED STABLE)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key: raise Exception("SECRET_MISSING: ANTHROPIC_API_KEY NOT FOUND")
        
        # อัปเกรดโมเดลฟรีที่เสถียรที่สุดในปัจจุบัน (Google Gemini 2.0 Flash)
        # ตัวเดิม meta-llama... มักจะเกิดปัญหา "No endpoints found" บน OpenRouter
        target_model = "google/gemini-2.0-flash-001:free"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://aegis.watsystems.tech",
            "X-Title": "AEGIS Sovereign Authority",
        }
        
        data = {
            "model": target_model,
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        "You are AEGIS, the elite Logic Auditor by WAT SYSTEMS. "
                        "Scan the payload for structural failures. Be brutal and decisive. "
                        "Output ONLY a valid JSON object: "
                        "{\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                    )
                },
                {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:12000]}"}
            ],
            "temperature": 0.0,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=60)
        
        if response.status_code != 200:
            err_msg = response.json().get("error", {}).get("message", "API Communication Failure")
            raise Exception(f"API_REJECTION: {err_msg}")
            
        result = response.json()
        if "choices" not in result:
            raise Exception("INVALID_REPLY: API returned no logic choices.")
            
        content = result['choices'][0]['message']['content'].strip()
        
        # Robust JSON cleaning
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"): content = content[4:]
            content = content.split("```")[0].strip()
            
        return json.loads(content)
        
    except Exception as e:
        send_telegram_alert(0, str(e), status="CRITICAL_FAILURE")
        return {
            "trust_score": 0, 
            "findings": [{
                "issue": "SYSTEM UPLINK SEVERED", 
                "catastrophic_impact": str(e), 
                "the_cure": "Ensure API key is sk-or-v1... and has free model access enabled."
            }]
        }

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='header-container'>
        <div class='brand-name'>AEGIS</div>
        <div class='brand-motto'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# Pillar Matrix
st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-item'><span class='pillar-id'>AUDIT P-01</span><span class='pillar-name'>CODE SECURITY</span></div>
        <div class='pillar-item'><span class='pillar-id'>AUDIT P-02</span><span class='pillar-name'>WORKFLOW</span></div>
        <div class='pillar-item'><span class='pillar-id'>AUDIT P-03</span><span class='pillar-name'>SMART CONTRACTS</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD FOR DISSECTION:", height=320, placeholder="Paste architectural logic or source code for supreme audit...")

if st.button("INITIATE GLOBAL AUDIT"):
    if not payload.strip():
        st.error("ERROR: SYSTEM REQUIRES DATA PAYLOAD.")
    else:
        with st.spinner("Decoding structural integrity..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            
            # Successful Alert
            if st.session_state.result:
                score = st.session_state.result.get('trust_score', 0)
                issue = st.session_state.result.get('findings', [{}])[0].get('issue', 'Unknown')
                if score > 0 or issue != "SYSTEM UPLINK SEVERED":
                    send_telegram_alert(score, issue, status="SUCCESS")
                
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE RESULTS (SOVEREIGN REVEAL)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-value'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#3fb950; color:#0d1117; display:inline-block; padding:4px 12px; border-radius:4px; font-size:11px; font-weight:900; letter-spacing:1px;'>VALIDATED BY AEGIS CORE</div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='alert-box'>
                <div class='alert-title'>● FATAL FLAW DETECTED</div>
                <div class='alert-body'>{f.get('issue')}</div>
                <div style='margin-top:20px; font-size:13px; color:#8b949e; line-height:1.6;'>
                    <b>CATASTROPHIC IMPACT:</b><br>{f.get('catastrophic_impact')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.link_button("BROADCAST AUTHORITY ON X", f"[https://twitter.com/intent/tweet?text=Logic](https://twitter.com/intent/tweet?text=Logic) score {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️ Test at AEGIS.", use_container_width=True)

        # Paywall
        st.write("")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='paywall-container'>
                    <div style='color:#e3b341; font-weight:900; font-size:11px; letter-spacing:3px; margin-bottom:12px;'>REMEDIATION ENCRYPTED</div>
                    <div style='color:#8b949e; font-size:13px; margin-bottom:25px;'>Remediation code is restricted to Enterprise Pass holders.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE ENTERPRISE PASS ($9)", "[https://porschza.gumroad.com/l/AEGIS](https://porschza.gumroad.com/l/AEGIS)", type="primary", use_container_width=True)
            
            passcode = st.text_input("ACCESS PASSCODE:", type="password")
            if st.button("DECRYPT SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("Access Denied.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.markdown("### 🟢 TECHNICAL SOLUTION")
            st.code(f.get('the_cure'), language='python')

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET SYSTEM"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#30363d; font-size:10px; margin-top:100px; font-weight:700; letter-spacing:4px;'>WAT SYSTEMS | AEGIS v13.1 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
