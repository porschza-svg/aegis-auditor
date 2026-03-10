import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. ARCHITECTURAL UI AUTHORITY (THE SINGULARITY STYLING)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="WAT SYSTEMS | AEGIS", 
    layout="centered", 
    page_icon="🛡️"
)

# Initialize Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Inter:wght@400;900&display=swap');

    /* Global Authority Reset */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { 
        background: radial-gradient(circle at 50% -20%, #1a1f2e 0%, #05070a 60%);
        color: #e6edf3; 
        font-family: 'Inter', sans-serif; 
    }

    /* Cinematic Logo Section */
    .hero-box {
        text-align: center;
        padding: 80px 0 40px 0;
    }
    .logo-main {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 5rem;
        letter-spacing: 25px;
        color: #ffffff;
        margin-right: -25px; /* Offset for letter spacing center */
        text-shadow: 0 0 80px rgba(88, 166, 255, 0.2);
        animation: glow 4s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(88, 166, 255, 0.1); }
        to { text-shadow: 0 0 50px rgba(88, 166, 255, 0.4); }
    }
    .brand-sub {
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 8px;
        color: #58a6ff;
        text-transform: uppercase;
        margin-top: -10px;
        opacity: 0.8;
    }

    /* Terminal Input Authority */
    .stTextArea textarea {
        background-color: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid #30363d !important;
        border-radius: 4px !important;
        color: #3fb950 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        padding: 25px !important;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5) !important;
    }

    /* Cyber Pillars - Matrix Layout */
    .pillar-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-bottom: 40px;
    }
    .pillar {
        background: rgba(22, 27, 34, 0.5);
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 4px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .pillar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: #58a6ff;
        opacity: 0.3;
    }
    .pillar-title { font-weight: 900; font-size: 11px; letter-spacing: 2px; color: #8b949e; text-transform: uppercase; }

    /* Authority Button */
    div.stButton > button {
        background: #f0f6fc !important;
        color: #0d1117 !important;
        font-weight: 900 !important;
        border-radius: 4px !important;
        padding: 15px 40px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border: none !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        background: #58a6ff !important;
        color: #ffffff !important;
        transform: scale(1.01);
    }

    /* The Reveal (Result Section) */
    .result-aura {
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 60px;
        border-radius: 4px;
        text-align: center;
        margin: 50px 0;
        border-left: 1px solid #58a6ff;
        box-shadow: -20px 0 50px rgba(88, 166, 255, 0.05);
    }
    .trust-value {
        font-size: 120px;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(180deg, #ffffff 0%, #30363d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Critical Flaw Box */
    .flaw-authority {
        background: rgba(248, 81, 73, 0.03);
        border: 1px solid rgba(248, 81, 73, 0.2);
        padding: 40px;
        margin-top: 30px;
        border-right: 5px solid #f85149;
    }
    .flaw-label { color: #f85149; font-weight: 900; letter-spacing: 3px; font-size: 12px; margin-bottom: 20px; }

    /* Sovereign Paywall */
    .sovereign-lock {
        background: #000;
        border: 1px solid #e3b341;
        padding: 60px;
        text-align: center;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. AUDIT LOGIC (NEURAL CORE)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {"trust_score": 0, "findings": [{"issue": "UPLINK SEVERED", "severity": "CRITICAL", "catastrophic_impact": "System Secrets Missing.", "the_cure": "Configure API Key."}]}
        
        # Engine: Using Llama 3.1 8B Free for initial scan
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis-auditor.streamlit.app",
                "X-Title": "AEGIS SINGULARITY",
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are AEGIS, a supreme Logic Auditor. Analyze strictly. Output JSON ONLY."},
                    {"role": "user", "content": f"PAYLOAD:\n{payload[:10000]}"}
                ],
                "temperature": 0.1,
                "response_format": {"type": "json_object"}
            })
        )
        
        result = response.json()
        raw_content = result['choices'][0]['message']['content'].strip()
        return json.loads(raw_content)
    except Exception as e:
        return {"trust_score": 0, "findings": [{"issue": "CORE ERROR", "severity": "CRITICAL", "catastrophic_impact": str(e), "the_cure": "Check Uplink."}]}

# ────────────────────────────────────────────────
# 3. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='hero-box'>
        <div class='logo-main'>AEGIS</div>
        <div class='brand-sub'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# Status Matrix
st.markdown("""
    <div class='pillar-grid'>
        <div class='pillar'><div class='pillar-title'>CODE SECURITY</div></div>
        <div class='pillar'><div class='pillar-title'>WORKFLOW LOGIC</div></div>
        <div class='pillar'><div class='pillar-title'>SMART CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD FOR DISSECTION:", height=300, placeholder="/// INITIATE UPLINK BY PASTING TARGET DATA")

if st.button("EXECUTE NEURAL SCAN"):
    if not payload.strip():
        st.error("SYSTEM ERROR: NULL PAYLOAD.")
    else:
        with st.spinner("QUANTUM SCAN IN PROGRESS..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 4. THE REVEAL
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown(f"""
        <div class='result-aura'>
            <div style='color: #8b949e; letter-spacing: 8px; font-weight: 900; font-size: 14px;'>LOGIC INTEGRITY</div>
            <div class='trust-value'>{score}%</div>
            <div style='color: #58a6ff; font-weight: 800; letter-spacing: 4px; font-size: 10px; margin-top: 20px;'>AUTHENTICATED BY AEGIS CORE</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Matrix
    st.link_button("𝕏 BROADCAST RESULTS ON X", f"https://twitter.com/intent/tweet?text=Logic Authority Scanned. Score: {score}%. 🛡️ Test at AEGIS.", use_container_width=True)
    
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='flaw-authority'>
                <div class='flaw-label'>● DETECTED FATAL FLAW</div>
                <div style='font-size: 20px; font-weight: 900; color: #ffffff; margin-bottom: 20px;'>{f.get('issue')}</div>
                <div style='color: #8b949e; font-size: 11px; font-weight: 800; margin-bottom: 10px;'>CATASTROPHIC IMPACT:</div>
                <div style='font-style: italic; line-height: 1.8; color: #e6edf3;'>"{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Sovereign Paywall
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='sovereign-lock'>
                    <div style='color: #e3b341; font-weight: 900; letter-spacing: 10px; font-size: 12px; margin-bottom: 30px;'>REMEDIATION ENCRYPTED</div>
                    <div style='color: #8b949e; font-size: 13px; margin-bottom: 40px;'>Remediation code is restricted to Sovereign Enterprise holders.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("👉 SECURE SOVEREIGN PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            st.write("")
            passcode = st.text_input("ENTER ACCESS PASSCODE:", type="password")
            if st.button("🔓 DECRYPT SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("ACCESS DENIED.")
        else:
            st.success("SOVEREIGN ACCESS GRANTED")
            st.code(f.get('the_cure'))

    if st.button("🔄 RESET SYSTEM"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#30363d; font-size:9px; margin-top:100px; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v12.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
