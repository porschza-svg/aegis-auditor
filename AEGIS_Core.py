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

# Initialize Session States for Persistence
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# Global CSS: Clean, High-Contrast, Professional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { 
        background-color: #0d1117; 
        color: #c9d1d9; 
        font-family: 'Inter', sans-serif; 
    }

    /* Brand Header: The Sovereign Look */
    .header-container { text-align: left; border-left: 3px solid #58a6ff; padding-left: 20px; margin: 40px 0; }
    .brand-name { font-weight: 900; font-size: 2.2rem; letter-spacing: -1px; color: #ffffff; margin-bottom: 0; }
    .brand-motto { font-size: 10px; font-weight: 700; color: #8b949e; letter-spacing: 4px; text-transform: uppercase; }

    /* Matrix Status Indicators */
    .pillar-row { display: flex; gap: 12px; margin-bottom: 30px; }
    .pillar-item { 
        flex: 1; 
        background: #161b22; 
        border: 1px solid #30363d; 
        padding: 12px; 
        border-radius: 6px; 
        text-align: center;
    }
    .pillar-id { font-size: 8px; font-weight: 800; color: #58a6ff; display: block; }
    .pillar-name { font-size: 11px; font-weight: 600; color: #f0f6fc; }

    /* Input Terminal */
    .stTextArea textarea { 
        background-color: #010409 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 8px !important; 
        color: #e6edf3 !important; 
        font-family: 'SF Mono', 'Fira Code', monospace !important;
        font-size: 14px !important;
        padding: 20px !important;
        line-height: 1.6;
    }

    /* Action Button: Premium Heavyweight */
    div.stButton > button {
        background: #238636 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        padding: 18px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: 0.2s all;
    }
    div.stButton > button:hover { background: #2ea043 !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(35,134,54,0.3); }

    /* Result Aesthetics */
    .result-card { 
        background: #0d1117; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        padding: 40px; 
        margin-top: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    .score-label { font-size: 11px; font-weight: 800; color: #8b949e; letter-spacing: 2px; }
    .score-value { font-size: 84px; font-weight: 900; color: #ffffff; line-height: 1; margin: 10px 0; }
    
    .alert-box { 
        background: rgba(248, 81, 73, 0.1); 
        border-left: 4px solid #f85149; 
        padding: 24px; 
        border-radius: 0 8px 8px 0;
        margin-top: 25px;
    }
    .alert-title { color: #f85149; font-weight: 800; font-size: 13px; text-transform: uppercase; margin-bottom: 8px; }
    .alert-body { font-size: 16px; font-weight: 600; color: #f0f6fc; line-height: 1.5; }

    /* Paywall: Exclusive Look */
    .paywall-container { 
        background: #161b22; 
        border: 1px solid #e3b341; 
        padding: 30px; 
        border-radius: 8px; 
        text-align: center;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (NOTIFICATIONS)
# ────────────────────────────────────────────────
def send_telegram_alert(score, issue):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
        if token and chat_id:
            message = (
                f"🚨 *[AEGIS RADAR ALERT]*\n\n"
                f"● *Status:* Audit Complete\n"
                f"● *Logic Score:* {score}%\n"
                f"● *Primary Flaw:* {issue}\n\n"
                f"🛡️ _Authenticated by WAT SYSTEMS_"
            )
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
    except: pass

# ────────────────────────────────────────────────
# 3. PRECISE AUDIT ENGINE (CLAUDE 3.5 / LLAMA)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key: raise Exception("SYSTEM_SECRET_ERROR: API_KEY_NOT_FOUND")
        
        # สำหรับโหมด "ฟรีเมี่ยม": เราใช้โมเดลรุ่นฟรีแต่ประมวลผลด้วยตรรกะระดับสูง
        target_model = "meta-llama/llama-3.1-8b-instruct:free"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://aegis.watsystems.tech",
            "X-Title": "AEGIS Sovereign Audit",
        }
        
        data = {
            "model": target_model,
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        "You are AEGIS, the supreme Logic Auditor by WAT SYSTEMS. "
                        "Identify the SINGLE most dangerous logic flaw. Be cold, expert, and brutal. "
                        "Output ONLY a valid JSON object: "
                        "{\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                    )
                },
                {"role": "user", "content": f"PAYLOAD TO DISSECT:\n{payload[:10000]}"}
            ],
            "temperature": 0.0,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=45)
        
        # Error Handling เชิงลึก
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Uplink Failed")
            raise Exception(f"API_REJECTION: {error_msg}")
            
        result = response.json()
        
        if "choices" not in result:
            raise Exception("UNEXPECTED_RESPONSE: No analysis choices returned.")
            
        content = result['choices'][0]['message']['content'].strip()
        
        # Clean potential markdown wrap
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"): content = content[4:]
            content = content.split("```")[0].strip()
            
        return json.loads(content)
        
    except Exception as e:
        return {
            "trust_score": 0, 
            "findings": [{
                "issue": "CORE UPLINK ERROR", 
                "catastrophic_impact": str(e), 
                "the_cure": "Ensure API Credits are active and Secrets are configured."
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

# Status Matrix (Fixed Regression)
st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-item'><span class='pillar-id'>P-01</span><span class='pillar-name'>CODE SECURITY</span></div>
        <div class='pillar-item'><span class='pillar-id'>P-02</span><span class='pillar-name'>WORKFLOW</span></div>
        <div class='pillar-item'><span class='pillar-id'>P-03</span><span class='pillar-name'>SMART CONTRACTS</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=300, placeholder="Paste architectural logic or source code for authoritative dissection...")

if st.button("EXECUTE GLOBAL AUDIT"):
    if not payload.strip():
        st.error("SYSTEM ERROR: Null payload detected.")
    else:
        with st.spinner("Decoding structural DNA..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            
            # Send Telegram Alert
            if st.session_state.result:
                score = st.session_state.result.get('trust_score', 0)
                issue = st.session_state.result.get('findings', [{}])[0].get('issue', 'Unknown')
                send_telegram_alert(score, issue)
                
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (RESULT ARCHITECTURE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-value'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#3fb950; color:#0d1117; display:inline-block; padding:2px 8px; border-radius:3px; font-size:10px; font-weight:900;'>AUDIT SEALED</div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='alert-box'>
                <div class='alert-title'>● DETECTED FATAL FLAW</div>
                <div class='alert-body'>{f.get('issue')}</div>
                <div style='margin-top:15px; font-size:12px; color:#8b949e;'>
                    <b>IMPACT:</b> {f.get('catastrophic_impact')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.link_button("SHARE AUTHORITY ON X", f"[https://twitter.com/intent/tweet?text=Logic](https://twitter.com/intent/tweet?text=Logic) Authority Scanned. Score: {score}%. 🛡️ Test yours at AEGIS.", use_container_width=True)

        # Sovereign Paywall (Premium Path)
        st.write("")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='paywall-container'>
                    <div style='color:#e3b341; font-weight:900; font-size:10px; letter-spacing:2px; margin-bottom:10px;'>REMEDIATION RESTRICTED</div>
                    <div style='color:#8b949e; font-size:12px; margin-bottom:20px;'>Enterprise pass required to decrypt the technical solution.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE ENTERPRISE PASS ($9)", "[https://porschza.gumroad.com/l/AEGIS](https://porschza.gumroad.com/l/AEGIS)", type="primary", use_container_width=True)
            
            passcode = st.text_input("ACCESS PASSCODE:", type="password", key="pass_input")
            if st.button("DECRYPT REMEDIATION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("Access Denied.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.markdown("### 🟢 TECHNICAL SOLUTION")
            st.code(f.get('the_cure'), language='python')

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#30363d; font-size:10px; margin-top:80px; font-weight:700; letter-spacing:3px;'>WAT SYSTEMS | AEGIS v13.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
