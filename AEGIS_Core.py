import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. INDUSTRIAL AUTHORITY UI SYSTEM
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

# Professional Industrial Styling (Strict Grayscale & High Contrast)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono:wght@500&display=swap');
    
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { 
        background-color: #0d1117; 
        color: #e6edf3; 
        font-family: 'Inter', sans-serif; 
    }

    /* Sovereign Brand Header */
    .header-box { 
        border-bottom: 2px solid #30363d; 
        padding-bottom: 30px; 
        margin-bottom: 50px; 
        margin-top: 40px; 
    }
    .logo-main { 
        font-weight: 900; 
        font-size: 2.5rem; 
        letter-spacing: -1px; 
        color: #ffffff; 
        margin: 0; 
        line-height: 1;
    }
    .logo-sub { 
        font-size: 10px; 
        font-weight: 700; 
        color: #8b949e; 
        letter-spacing: 5px; 
        text-transform: uppercase; 
        margin-top: 8px;
    }

    /* Industrial Pillars Matrix */
    .pillar-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 30px; }
    .pillar-item { 
        background: #161b22; 
        border: 1px solid #30363d; 
        padding: 15px; 
        border-radius: 4px; 
        text-align: center;
    }
    .p-tag { font-size: 8px; font-weight: 900; color: #58a6ff; display: block; margin-bottom: 4px; }
    .p-name { font-size: 11px; font-weight: 700; color: #f0f6fc; text-transform: uppercase; }

    /* The Terminal Interface */
    .stTextArea textarea { 
        background-color: #010409 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 4px !important; 
        color: #e6edf3 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        padding: 25px !important;
        line-height: 1.6;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; }

    /* Action Button: Executioner Style */
    div.stButton > button {
        background: #f0f6fc !important;
        color: #0d1117 !important;
        font-weight: 900 !important;
        border-radius: 4px !important;
        padding: 20px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        transition: 0.2s all;
    }
    div.stButton > button:hover { background: #58a6ff !important; color: #ffffff !important; }

    /* Result Architecture */
    .result-frame { 
        background: #0d1117; 
        border: 1px solid #30363d; 
        padding: 50px; 
        margin-top: 50px; 
        border-radius: 4px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5);
    }
    .score-label { font-size: 11px; font-weight: 800; color: #8b949e; letter-spacing: 3px; }
    .score-value { font-size: 96px; font-weight: 900; color: #ffffff; line-height: 1; margin: 15px 0; }
    
    .flaw-box { 
        background: rgba(248, 81, 73, 0.03); 
        border: 1px solid rgba(248, 81, 73, 0.2); 
        border-left: 5px solid #f85149; 
        padding: 30px; 
        margin-top: 30px;
    }
    .flaw-head { color: #f85149; font-weight: 900; font-size: 13px; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase; }
    .flaw-impact { font-size: 16px; font-weight: 600; color: #f0f6fc; line-height: 1.6; }

    .locked-area { background: #161b22; border: 1px solid #e3b341; padding: 40px; text-align: center; margin-top: 30px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (PRIORITY UPLINK)
# ────────────────────────────────────────────────
def broadcast_radar(score, flaw, status="ACTIVE"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
        if token and chat_id:
            msg = (
                f"🛡️ *[AEGIS RADAR]*\n\n"
                f"● *STATUS:* {status}\n"
                f"● *SCORE:* {score}%\n"
                f"● *ISSUE:* {flaw}\n\n"
                f"📡 _Authority: WAT SYSTEMS_"
            )
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, 
                          timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME LOGIC ENGINE (STABLE & PRECISE)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    # ยิง Telegram ทันทีที่เริ่มงาน
    broadcast_radar(0, "ANALYSIS_INITIATED", "UPLINKING")
    
    # ดึง Key ทุกรูปแบบที่เป็นไปได้เพื่อป้องกันความผิดพลาดของสถาปนิก
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        return {"trust_score": 0, "findings": [{"issue": "UPLINK SEVERED", "catastrophic_impact": "Missing API Key in Secrets.", "the_cure": "Set OPENROUTER_API_KEY."}]}

    try:
        # ใช้โมเดลที่เสถียรกว่า Llama 3.1 ในช่วง Free Tier ของ OpenRouter
        # google/gemini-flash-1.5 เป็นรุ่นที่พรีเมี่ยมที่สุดที่ยังเสถียรในโหมดฟรี
        target_model = "google/gemini-flash-1.5"
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis.watsystems.tech",
                "X-Title": "AEGIS Industrial Standard",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": target_model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are AEGIS, a professional Industrial Logic Auditor. Analyze strictly. Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                    },
                    {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:15000]}"}
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            }),
            timeout=40
        )
        
        # ตรวจสอบ API Response อย่างละเอียด
        if response.status_code != 200:
            err_msg = response.json().get('error', {}).get('message', 'Uplink Refused')
            raise Exception(f"API_ERROR: {err_msg}")
            
        result = response.json()
        
        # 🚨 FIX: ป้องกันปัญหา KeyError 'choices'
        if "choices" not in result:
            err_info = result.get('error', {}).get('message', str(result))
            raise Exception(f"INVALID_DATA: {err_info}")
            
        raw_content = result['choices'][0]['message']['content'].strip()
        data = json.loads(raw_content)
        
        # ส่ง Radar สรุปผล
        broadcast_radar(data.get('trust_score', 0), data['findings'][0]['issue'], "COMPLETE")
        
        return data
        
    except Exception as e:
        broadcast_radar(0, str(e)[:50], "FAILURE")
        return {
            "trust_score": 0, 
            "findings": [{
                "issue": "CORE ERROR", 
                "catastrophic_impact": str(e), 
                "the_cure": "Check API Credits or Endpoint Availability."
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

# Status Matrix Pillars
st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-item'><span class='p-tag'>MOD-01</span><span class='p-name'>CODE SECURITY</span></div>
        <div class='pillar-item'><span class='p-tag'>MOD-02</span><span class='p-name'>WORKFLOW</span></div>
        <div class='pillar-item'><span class='p-tag'>MOD-03</span><span class='p-name'>CONTRACTS</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD FOR DISSECTION:", height=300, placeholder="/// PASTE ARCHITECTURAL DATA FOR AUDIT")

if st.button("RUN GLOBAL AUDIT"):
    if not payload.strip():
        st.error("ERROR: Null payload.")
    else:
        with st.spinner("Decoding structural DNA..."):
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
    
    st.markdown("<div class='result-frame'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-value'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#58a6ff; color:#000; padding:2px 10px; font-size:9px; font-weight:900;'>VALIDATED BY WAT SYSTEMS</div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='flaw-box'>
                <div class='flaw-head'>● FATAL FLAW DETECTED</div>
                <div class='flaw-impact'>{f.get('issue')}</div>
                <div style='margin-top:20px; font-size:12px; opacity:0.6; line-height:1.6;'>
                    <b>IMPACT:</b><br>{f.get('catastrophic_impact')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.link_button("BROADCAST AUTHORITY ON X", f"https://twitter.com/intent/tweet?text=Logic Authority Score: {score}%. 🛡️ Tested at AEGIS.", use_container_width=True)

        # Paywall Path
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='locked-area'>
                    <div style='color:#e3b341; font-weight:900; font-size:10px; letter-spacing:3px; margin-bottom:15px;'>REMEDIATION RESTRICTED</div>
                    <div style='color:#8b949e; font-size:12px; margin-bottom:25px;'>Enterprise pass required to decrypt the technical solution.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE ENTERPRISE PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            passcode = st.text_input("ACCESS PASSCODE:", type="password")
            if st.button("🔓 DECRYPT SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("Access Denied.")
        else:
            st.success("✅ ACCESS GRANTED")
            st.markdown("### 🔵 TECHNICAL SOLUTION")
            st.code(f.get('the_cure'), language='python')

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#30363d; font-size:9px; margin-top:100px; font-weight:700; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v17.0 | INDUSTRIAL AUTHORITY</div>", unsafe_allow_html=True)
