import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. VANGUARD ABSOLUTE UI (HIGH-FIDELITY AUTHORITY)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | VANGUARD", 
    layout="centered", 
    page_icon="🛡️"
)

# Persistent Engine State
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "WAT" Signature Premium CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=JetBrains+Mono:wght@400;700&display=swap');

    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { 
        background-color: #000000; 
        color: #ffffff; 
        font-family: 'Space Grotesk', sans-serif; 
    }

    /* Sovereign Vanguard Header */
    .vanguard-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px 0;
        margin-bottom: 50px;
        text-align: left;
    }
    .v-logo {
        font-weight: 700;
        font-size: 3rem;
        letter-spacing: -2px;
        color: #ffffff;
        margin: 0;
    }
    .v-sub {
        font-size: 9px;
        font-weight: 700;
        color: #58a6ff;
        letter-spacing: 6px;
        text-transform: uppercase;
        opacity: 0.8;
    }

    /* Pillars: Custom Flexbox Grid (Non-Default) */
    .pillar-flex {
        display: flex;
        gap: 10px;
        margin-bottom: 40px;
    }
    .pillar-box {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        padding: 15px;
        border-radius: 4px;
        text-align: left;
        border-left: 2px solid #30363d;
    }
    .pillar-label { font-size: 8px; color: #8b949e; font-weight: 700; text-transform: uppercase; }
    .pillar-val { font-size: 11px; font-weight: 700; color: #f0f6fc; margin-top: 4px; }

    /* The Obsidian Terminal */
    .stTextArea textarea { 
        background-color: #080808 !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 4px !important; 
        color: #e6edf3 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 25px !important;
        line-height: 1.6;
        box-shadow: inset 0 0 20px rgba(0,0,0,1) !important;
    }

    /* Heavyweight Execution Button */
    div.stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 2px !important;
        padding: 24px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        transition: 0.2s all;
    }
    div.stButton > button:hover { background: #58a6ff !important; color: white !important; }

    /* Result Revealed: High Contrast Mode */
    .reveal-frame {
        background: #000000;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 60px;
        margin-top: 60px;
        border-radius: 4px;
        border-top: 4px solid #58a6ff;
    }
    .reveal-score {
        font-size: 120px;
        font-weight: 700;
        letter-spacing: -8px;
        line-height: 1;
        margin: 20px 0;
    }
    
    /* Fatal Flaw: The Industrial Red Alert */
    .fatal-alert {
        background: rgba(248, 81, 73, 0.05);
        border: 1px solid rgba(248, 81, 73, 0.2);
        padding: 40px;
        margin-top: 40px;
        border-left: 8px solid #f85149;
    }
    .fatal-tag { color: #f85149; font-weight: 700; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; display: block; }
    .fatal-body { font-size: 20px; font-weight: 700; color: #ffffff; line-height: 1.4; }

    /* The Restricted Cure */
    .cure-lock {
        background: #050505;
        border: 1px solid #e3b341;
        padding: 50px;
        text-align: center;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (PRIORITY 0 UPLINK)
# ────────────────────────────────────────────────
def broadcast_radar(score, detail, status="AUDIT_START"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
        if token and chat_id:
            msg = (
                f"🛡️ *[AEGIS VANGUARD]*\n\n"
                f"● *STATUS:* {status}\n"
                f"● *TRUST:* {score}%\n"
                f"● *IMPACT:* {detail}\n\n"
                f"📡 _Authority: WAT SYSTEMS_"
            )
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, 
                          timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. VANGUARD ENGINE (RESILIENT API LOGIC)
# ────────────────────────────────────────────────
def execute_aegis_audit(payload):
    # ยิง Radar ทันทีแบบไม่ต้องรอ
    broadcast_radar(0, "Initiating Neural Scan...", "UPLINKING")
    
    # ดึง Key แบบยืดหยุ่น (ลองทั้งสองชื่อที่เคยใช้)
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        return {"trust_score": 0, "findings": [{"issue": "UPLINK SEVERED", "catastrophic_impact": "Secrets Missing: OPENROUTER_API_KEY", "the_cure": "Configure Streamlit Secrets."}]}

    try:
        # ใช้ Model ที่เสถียรที่สุดในหมวดพรีเมี่ยมฟรี
        target_model = "google/gemini-2.0-flash-001:free"
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis.watsystems.tech",
                "X-Title": "AEGIS VANGUARD",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": target_model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are AEGIS, the Supreme Industrial Auditor. Dissect input for ONE fatal flaw. Be factual, cold. JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                    },
                    {"role": "user", "content": f"AUDIT_PAYLOAD:\n{payload[:15000]}"}
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            }),
            timeout=40
        )
        
        if response.status_code != 200:
            err_msg = response.json().get('error', {}).get('message', 'Uplink Refused')
            raise Exception(f"API_REJECTION: {err_msg}")
            
        result = response.json()
        
        # ดักจับ KeyError: 'choices' ที่เคยพลาด
        if "choices" not in result:
            msg = result.get('error', {}).get('message', 'Unknown Response Structure')
            raise Exception(f"DATA_FAILURE: {msg}")
            
        content = result['choices'][0]['message']['content'].strip()
        data = json.loads(content)
        
        # ยิง Radar สรุปผล
        broadcast_radar(data.get('trust_score', 0), data['findings'][0]['issue'], "COMPLETE")
        
        return data
        
    except Exception as e:
        broadcast_radar(0, str(e)[:50], "FAILURE")
        return {
            "trust_score": 0, 
            "findings": [{
                "issue": "CORE UPLINK FAILURE", 
                "catastrophic_impact": str(e), 
                "the_cure": "Check API Credits or Endpoint Availability."
            }]
        }

# ────────────────────────────────────────────────
# 4. SYSTEM INTERFACE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='vanguard-header'>
        <div class='v-logo'>AEGIS</div>
        <div class='v-sub'>WAT SYSTEMS | VANGUARD ABSOLUTE AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# Custom Pillars Matrix
st.markdown("""
    <div class='pillar-flex'>
        <div class='pillar-box'><span class='pillar-label'>SCAN P-01</span><div class='pillar-val'>CODE SECURITY</div></div>
        <div class='pillar-box'><span class='pillar-label'>SCAN P-02</span><div class='pillar-val'>WORKFLOW LOGIC</div></div>
        <div class='pillar-box'><span class='pillar-label'>SCAN P-03</span><div class='pillar-val'>SMART CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=300, placeholder="/// PASTE ARCHITECTURAL DATA FOR DISSECTION")

if st.button("EXECUTE SUPREME SCAN"):
    if not payload.strip():
        st.error("SYSTEM ERROR: NULL DATA.")
    else:
        with st.spinner("Decoding structural DNA..."):
            st.session_state.result = execute_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. REVEAL ARCHITECTURE
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='reveal-frame'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 11px; font-weight: 700; color: #8b949e; letter-spacing: 4px;'>GLOBAL TRUST SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='reveal-score'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#58a6ff; color:#000; padding:4px 12px; font-size:10px; font-weight:700;'>VALIDATED BY WAT SYSTEMS</div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='fatal-alert'>
                <span class='fatal-tag'>● FATAL FLAW IDENTIFIED</span>
                <div class='fatal-body'>{f.get('issue')}</div>
                <div style='margin-top:20px; font-size:13px; color:#8b949e; line-height:1.6;'>
                    <b>IMPACT:</b><br>{f.get('catastrophic_impact')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.link_button("BROADCAST AUTHORITY ON X", f"https://twitter.com/intent/tweet?text=Logic score {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️", use_container_width=True)

        if not st.session_state.unlocked:
            st.markdown("""
                <div class='cure-lock'>
                    <div style='color:#e3b341; font-weight:700; font-size:11px; letter-spacing:4px; margin-bottom:15px;'>REMEDIATION RESTRICTED</div>
                    <div style='color:#8b949e; font-size:12px; margin-bottom:25px;'>Sovereign enterprise pass required for remediation deployment.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE ENTERPRISE PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            passcode = st.text_input("INPUT ACCESS PASSCODE:", type="password")
            if st.button("🔓 DECRYPT SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("Access Denied.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.markdown("### 🟢 TECHNICAL SOLUTION")
            st.code(f.get('the_cure'), language='python')

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET VANGUARD"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#222; font-size:9px; margin-top:100px; font-weight:700; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v19.0 | VANGUARD AUTHORITY</div>", unsafe_allow_html=True)
