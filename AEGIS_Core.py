import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. SOVEREIGN INDUSTRIAL UI (PREMIUM AUTHORITY)
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

# High-Contrast Industrial Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@500&display=swap');
    
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #050505; color: #e6edf3; font-family: 'Inter', sans-serif; }

    /* Header: Authority Branding */
    .header-box { border-left: 4px solid #58a6ff; padding-left: 20px; margin: 50px 0; }
    .logo-main { font-weight: 900; font-size: 2.5rem; letter-spacing: -1px; color: #ffffff; margin: 0; }
    .logo-sub { font-size: 10px; font-weight: 700; color: #8b949e; letter-spacing: 5px; text-transform: uppercase; }

    /* Matrix Pillars */
    .pillar-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 40px; }
    .pillar-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 4px; text-align: center; }
    .pillar-id { font-size: 8px; font-weight: 900; color: #58a6ff; text-transform: uppercase; display: block; }
    .pillar-name { font-size: 11px; font-weight: 700; color: #f0f6fc; }

    /* Input: Industrial Terminal */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 8px !important; 
        color: #3fb950 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        padding: 20px !important;
        line-height: 1.6;
    }

    /* Execution Button */
    div.stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 4px !important;
        padding: 20px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        transition: 0.3s all ease;
    }
    div.stButton > button:hover { background: #58a6ff !important; color: #ffffff !important; transform: scale(1.01); }

    /* Result Displays */
    .result-aura { background: #0d1117; border: 1px solid #30363d; padding: 50px; border-radius: 8px; margin-top: 50px; }
    .score-label { font-size: 11px; font-weight: 800; color: #8b949e; letter-spacing: 3px; }
    .score-value { font-size: 90px; font-weight: 900; color: #ffffff; line-height: 1; margin: 10px 0; letter-spacing: -4px; }
    
    .flaw-frame { border: 1px solid rgba(248, 81, 73, 0.3); border-left: 6px solid #f85149; padding: 30px; border-radius: 4px; margin-top: 30px; background: rgba(248,81,73,0.02); }
    .flaw-title { color: #f85149; font-weight: 900; font-size: 18px; text-transform: uppercase; margin-bottom: 15px; }
    
    .cure-zone { background: #000000; border: 1px solid #e3b341; padding: 40px; border-radius: 8px; text-align: center; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (SUPREME PRIORITY)
# ────────────────────────────────────────────────
def trigger_radar_alert(score, status, detail):
    try:
        # ดึงค่าจาก Secrets โดยตรง
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
        if token and chat_id:
            msg = (
                f"🛡️ *[AEGIS AUTHORITY RADAR]*\n\n"
                f"● *STATUS:* {status}\n"
                f"● *SCORE:* {score}%\n"
                f"● *IDENTIFIED:* {detail}\n\n"
                f"📡 _Operational Link: WAT SYSTEMS_"
            )
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, 
                          timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME AUDIT ENGINE (PRECISION LOGIC)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    # รองรับทั้งสองชื่อเพื่อความยืดหยุ่นของสถาปนิก
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        trigger_radar_alert(0, "SYSTEM_FAILURE", "Missing API Key")
        return {"trust_score": 0, "findings": [{"issue": "SECRET_MISSING", "catastrophic_impact": "Uplink severed. Auditor is blind.", "the_cure": "Check Streamlit Secrets for OPENROUTER_API_KEY."}]}

    try:
        # ใช้เครื่องยนต์ฟรีที่แรงที่สุด (Gemini 2.0 Flash) เพื่อความเป็น "พรีเมี่ยม"
        target_model = "google/gemini-2.0-flash-001:free"
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis.watsystems.tech",
                "X-Title": "AEGIS v15.0",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": target_model,
                "messages": [
                    {"role": "system", "content": "You are AEGIS, the supreme Logic Auditor. Analyze strictly. Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                    {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:12000]}"}
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            }),
            timeout=45
        )
        
        # ตรวจสอบสถานะการเชื่อมต่อทันที
        if response.status_code != 200:
            err_data = response.json()
            err_msg = err_data.get("error", {}).get("message", "Uplink Denied")
            raise Exception(f"API_REJECTION: {err_msg}")
            
        result = response.json()
        raw_content = result['choices'][0]['message']['content'].strip()
        audit_data = json.loads(raw_content)
        
        # ส่ง Radar ทันทีที่การวิเคราะห์สำเร็จ
        trigger_radar_alert(audit_data.get('trust_score', 0), "AUDIT_SUCCESS", audit_data['findings'][0]['issue'])
        
        return audit_data
        
    except Exception as e:
        trigger_radar_alert(0, "CORE_UPLINK_ERROR", str(e)[:100])
        return {
            "trust_score": 0, 
            "findings": [{
                "issue": "CORE UPLINK SEVERED", 
                "catastrophic_impact": str(e), 
                "the_cure": "Ensure API Key is valid and model 'google/gemini-2.0-flash-001:free' is accessible."
            }]
        }

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='header-box'>
        <div class='logo-main'>AEGIS</div>
        <div class='logo-sub'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# Pillar Grid
st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-box'><span class='pillar-id'>AUDIT-01</span><span class='pillar-name'>CODE SECURITY</span></div>
        <div class='pillar-box'><span class='pillar-id'>AUDIT-02</span><span class='pillar-name'>WORKFLOW</span></div>
        <div class='pillar-box'><span class='pillar-id'>AUDIT-03</span><span class='pillar-name'>CONTRACTS</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=320, placeholder="/// INITIATE UPLINK BY PASTING ARCHITECTURAL DATA")

if st.button("EXECUTE SUPREME AUDIT"):
    if not payload.strip():
        st.error("ERROR: SYSTEM REQUIRES DATA PAYLOAD.")
    else:
        with st.spinner("Decoding structural integrity..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. AUDIT REVEAL
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-value'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#58a6ff; color:#000000; display:inline-block; padding:3px 10px; border-radius:2px; font-size:10px; font-weight:900;'>AUTHENTICATED BY WAT SYSTEMS</div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='flaw-frame'>
                <div class='flaw-title'>⚠️ {f.get('issue')}</div>
                <div style='color: #8b949e; font-size: 11px; font-weight: 800; margin-bottom: 8px; text-transform: uppercase;'>Catastrophic Impact:</div>
                <div style='font-style: italic; line-height: 1.6; color: #e6edf3;'>"{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.link_button("BROADCAST RESULTS ON X", f"https://twitter.com/intent/tweet?text=Logic Authority Scanned. Score: {score}%. 🛡️ Verified by WAT SYSTEMS.", use_container_width=True)

        # Paywall
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='cure-zone'>
                    <div style='color:#e3b341; font-weight:900; font-size:11px; letter-spacing:4px; margin-bottom:15px;'>REMEDIATION ENCRYPTED</div>
                    <div style='color:#8b949e; font-size:12px; margin-bottom:25px;'>Remediation code is restricted to Sovereign Enterprise holders.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE SOVEREIGN PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            passcode = st.text_input("ACCESS PASSCODE:", type="password")
            if st.button("🔓 DECRYPT SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("ACCESS DENIED.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.code(f.get('the_cure'), language='python')

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#222222; font-size:9px; margin-top:100px; font-weight:700; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v15.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
