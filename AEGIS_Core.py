import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. OBSIDIAN AUTHORITY UI (PREMIUM ARCHITECTURE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | UNIVERSAL AUTHORITY", 
    layout="centered", 
    page_icon="🛡️"
)

# Persistence Control
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# High-Fidelity Professional Styling (Demolishing the "Student" Look)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { 
        background-color: #050505; 
        color: #e6edf3; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }

    /* Sovereign Header */
    .brand-header { padding: 80px 0 40px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 50px; }
    .logo-main { font-weight: 800; font-size: 3rem; letter-spacing: -2px; color: #ffffff; margin: 0; line-height: 1; }
    .logo-sub { font-size: 10px; font-weight: 700; color: #58a6ff; letter-spacing: 7px; text-transform: uppercase; margin-top: 10px; opacity: 0.8; }

    /* Industrial Pillars Matrix */
    .pillar-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 40px; }
    .pillar-box { 
        background: #0a0a0a; 
        border: 1px solid #1a1a1a; 
        padding: 20px; 
        border-radius: 4px; 
        border-left: 3px solid #30363d;
    }
    .p-tag { font-size: 8px; font-weight: 800; color: #8b949e; text-transform: uppercase; }
    .p-val { font-size: 12px; font-weight: 700; color: #ffffff; margin-top: 5px; }

    /* The Obsidian Terminal */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 4px !important; 
        color: #f0f6fc !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 30px !important;
        line-height: 1.7;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; }

    /* Premium Action Button (No more white block) */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 4px !important;
        padding: 22px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        transition: 0.2s all;
        margin-top: 20px;
    }
    div.stButton > button:hover { background-color: #58a6ff !important; color: white !important; transform: translateY(-2px); }

    /* Result Section: Authority Reveal */
    .result-aura { 
        background: #000000; 
        border: 1px solid #1a1a1a; 
        padding: 70px 50px; 
        margin-top: 70px; 
        border-top: 6px solid #58a6ff;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }
    .score-label { font-size: 11px; font-weight: 700; color: #8b949e; letter-spacing: 4px; text-transform: uppercase; }
    .score-val { font-size: 110px; font-weight: 800; color: #ffffff; letter-spacing: -8px; line-height: 1; margin: 20px 0; }
    
    /* Freemium Detailed Findings */
    .finding-card { 
        background: rgba(255,255,255,0.01); 
        border: 1px solid #1a1a1a; 
        padding: 35px; 
        border-radius: 4px; 
        margin-top: 25px; 
        border-left: 5px solid #f85149; 
    }
    .finding-title { font-weight: 800; color: #ffffff; font-size: 18px; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .finding-impact { font-size: 15px; color: #8b949e; line-height: 1.6; }

    /* The Cure Paywall: Luxurious Restriction */
    .cure-paywall { 
        background: #050505; 
        border: 1px solid #e3b341; 
        padding: 40px; 
        border-radius: 4px; 
        text-align: center; 
        margin-top: 20px;
    }
    .locked-tag { font-size: 9px; font-weight: 800; color: #e3b341; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px; display: block; }

    /* X-Share Loop */
    .x-share-btn { 
        display: inline-block; 
        background: #1da1f2; 
        color: white !important; 
        padding: 15px 35px; 
        border-radius: 50px; 
        text-decoration: none; 
        font-weight: 800; 
        font-size: 12px; 
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 30px;
        transition: 0.3s;
    }
    .x-share-btn:hover { background: #1a91da; transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (PRIORITY 0)
# ────────────────────────────────────────────────
def send_telegram_radar(score, issues):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = (
                f"🛡️ *[AEGIS AUTHORITY]*\n\n"
                f"● *STATUS:* Audit Successful\n"
                f"● *LOGIC SCORE:* {score}%\n"
                f"● *IDENTIFIED RISKS:* {len(issues)}\n\n"
                f"📡 _Authority: WAT SYSTEMS_"
            )
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME AUDIT ENGINE (HIGH-FIDELITY FREEMIUM)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key not configured.", "the_cure": "Set Secrets."}]}

    try:
        # ใช้โมเดลพรีเมี่ยมที่เสถียรที่สุด (Google Gemini 2.0 Flash) เพื่อเลี่ยง Error 404
        target_model = "google/gemini-2.0-flash-001:free"
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis.watsystems.tech",
                "X-Title": "AEGIS AUTHORITY",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": target_model,
                "messages": [
                    {
                        "role": "system", 
                        "content": (
                            "You are AEGIS, the supreme Logic Auditor by WAT SYSTEMS. "
                            "Scan for ALL dangerous logic flaws. Be factual, professional, and brutal. "
                            "Do not hold back on findings. Provide a detailed audit. "
                            "Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                        )
                    },
                    {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:15000]}"}
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            }),
            timeout=50
        )
        
        if response.status_code != 200:
            err = response.json().get('error', {}).get('message', 'Uplink Refused')
            raise Exception(f"API ERROR: {err}")
            
        result = response.json()
        raw_content = result['choices'][0]['message']['content'].strip()
        data = json.loads(raw_content)
        
        # ส่งเรดาร์แจ้งเตือน
        send_telegram_radar(data.get('trust_score', 0), data.get('findings', []))
        
        return data
        
    except Exception as e:
        return {"trust_score": 0, "findings": [{"issue": "CORE_UPLINK_FAILURE", "catastrophic_impact": str(e), "the_cure": "Check API Credentials or Credits."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='brand-header'>
        <div class='logo-main'>AEGIS</div>
        <div class='logo-sub'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-box'><span class='p-tag'>MOD-01</span><div class='p-name'>CODE AUDIT</div></div>
        <div class='pillar-box'><span class='p-tag'>MOD-02</span><div class='p-name'>LOGIC FLOW</div></div>
        <div class='pillar-box'><span class='p-tag'>MOD-03</span><div class='p-name'>WEB3 SECURITY</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD FOR DISSECTION:", height=300, placeholder="/// PASTE LOGIC DNA FOR SUPREME AUDIT")

if st.button("EXECUTE GLOBAL AUDIT (DETAILED SCAN)"):
    if not payload.strip():
        st.error("SYSTEM ERROR: NULL DATA.")
    else:
        with st.spinner("Decoding DNA..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (PREMIUM FREEMIUM)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #58a6ff; font-weight: 800; font-size: 11px; letter-spacing: 3px; margin-bottom: 30px;'>VALIDATED BY WAT SYSTEMS AUTHORITY</div>", unsafe_allow_html=True)
    
    # Viral Loop: แชร์คะแนนไป X
    share_msg = f"My project logic scored {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div style='text-align:center;'><a href='{share_url}' target='_blank' class='x-share-btn'>𝕏 SHARE YOUR AUTHORITY</a></div>", unsafe_allow_html=True)

    # Detailed Risks (The Premium Freemium Value)
    st.write("")
    st.subheader("🚨 DETECTED LOGIC FAILURES")
    findings = res.get("findings", [])
    
    for i, f in enumerate(findings):
        st.markdown(f"""
            <div class='finding-card'>
                <div class='finding-title'>RISK-{i+1:02}: {f.get('issue')}</div>
                <div class='finding-impact'><b>IMPACT ANALYSIS:</b> "{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall for The Cure
        if not st.session_state.unlocked:
            st.markdown(f"""
                <div class='cure-paywall'>
                    <span class='locked-tag'>🔒 REMEDIATION ENCRYPTED</span>
                    <div style='color:#8b949e; font-size:12px;'>Enterprise Pass required to decrypt technical solution for this vulnerability.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**THE CURE (TECHNICAL SOLUTION):**")
            st.code(f.get('the_cure'), language='python')

    # Premium Conversion
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 UNLOCK ALL TECHNICAL REMEDIATIONS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("ENTER ACCESS PASSCODE:", type="password")
        if st.button("🔓 DEPLOY SOLUTIONS"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS DENIED.")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#1a1a1a; font-size:10px; margin-top:120px; font-weight:700; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v25.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
