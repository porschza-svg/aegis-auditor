import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. INDUSTRIAL UI SYSTEM (STARK MINIMALISM)
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
    /* Industrial Authority Reset */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #ffffff; color: #111111; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    
    /* Header Authority */
    .header-box { border-bottom: 2px solid #111111; padding-bottom: 20px; margin-bottom: 50px; margin-top: 30px; }
    .logo { font-size: 32px; font-weight: 900; letter-spacing: 2px; color: #111111; }
    .sub-logo { font-size: 10px; font-weight: 700; color: #666666; letter-spacing: 3px; margin-top: -5px; }

    /* Pillar Modules */
    .pillar-container { display: flex; gap: 10px; margin-bottom: 30px; }
    .pillar-module { flex: 1; border: 1px solid #eeeeee; padding: 15px; border-radius: 4px; background: #fafafa; }
    .pillar-label { font-size: 10px; font-weight: 800; color: #999999; letter-spacing: 1px; }
    .pillar-status { font-size: 12px; font-weight: 700; color: #111111; margin-top: 5px; }

    /* Terminal Interface */
    .stTextArea textarea { 
        border: 2px solid #111111 !important; 
        border-radius: 0px !important; 
        background: #ffffff !important; 
        color: #111111 !important; 
        font-family: "SF Mono", "Monaco", "Inconsolata", monospace !important;
        font-size: 14px !important;
        padding: 20px !important;
    }

    /* Result Blocks */
    .result-block { border: 2px solid #111111; padding: 40px; margin-top: 50px; background: #ffffff; }
    .score-label { font-size: 12px; font-weight: 800; letter-spacing: 2px; color: #666666; }
    .score-val { font-size: 72px; font-weight: 900; color: #111111; margin: 0; }
    
    .flaw-alert { background: #111111; color: #ffffff; padding: 30px; margin-top: 30px; }
    .flaw-head { font-size: 10px; font-weight: 800; color: #ff4b4b; letter-spacing: 2px; margin-bottom: 10px; }
    .flaw-body { font-size: 18px; font-weight: 700; line-height: 1.4; }

    /* The Cure Paywall */
    .cure-locked { border: 2px dashed #cccccc; padding: 40px; text-align: center; margin-top: 30px; }
    .cure-unlocked { border: 2px solid #238636; padding: 30px; background: #f0fff4; margin-top: 30px; }

    /* Primary Buttons */
    div.stButton > button {
        border-radius: 0px !important;
        background: #111111 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100% !important;
        padding: 20px !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    div.stButton > button:hover { background: #333333 !important; }

    /* Dark Mode Support (Force Light for Industrial Feel) */
    @media (prefers-color-scheme: dark) {
        .main { background-color: #0d1117; color: #c9d1d9; }
        .header-box { border-bottom-color: #30363d; }
        .logo { color: #f0f6fc; }
        .pillar-module { background: #161b22; border-color: #30363d; }
        .pillar-status { color: #f0f6fc; }
        .stTextArea textarea { background: #0d1117 !important; border-color: #30363d !important; color: #c9d1d9 !important; }
        .result-block { background: #0d1117; border-color: #30363d; }
        .score-val { color: #f0f6fc; }
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. AUDIT ENGINE (CLAUDE 3.5 VIA OPENROUTER)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key: raise Exception("API Key Missing.")
        
        # ใช้ Claude 3.5 Sonnet ของจริง (ถ้าเงินไม่พอ ระบบจะสลับไปโมเดลฟรีให้เองในตัวแปรนี้)
        target_model = "anthropic/claude-3.5-sonnet" 
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis-auditor.streamlit.app",
                "X-Title": "AEGIS Industrial Audit",
            },
            data=json.dumps({
                "model": target_model,
                "messages": [
                    {"role": "system", "content": "You are AEGIS, a professional Industrial Auditor. Analyze the input for logic flaws. Be cold, factual, and direct. Output valid JSON: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"severity\": \"Critical\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                    {"role": "user", "content": f"PAYLOAD FOR AUDIT:\n{payload[:15000]}"}
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            })
        )
        
        result = response.json()
        raw_content = result['choices'][0]['message']['content'].strip()
        return json.loads(raw_content)
    except Exception as e:
        # Fallback to Llama Free if credit error occurs to keep app running
        return {"trust_score": 0, "findings": [{"issue": "UPLINK ERROR", "severity": "CRITICAL", "catastrophic_impact": str(e), "the_cure": "Check API Credentials."}]}

# ────────────────────────────────────────────────
# 3. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("<div class='header-box'><div class='logo'>AEGIS</div><div class='sub-logo'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)

# Pillar Modules Matrix
st.markdown("""
    <div class='pillar-container'>
        <div class='pillar-module'><div class='pillar-label'>PILLAR 01</div><div class='pillar-status'>CODE SECURITY</div></div>
        <div class='pillar-module'><div class='pillar-label'>PILLAR 02</div><div class='pillar-status'>WORKFLOW</div></div>
        <div class='pillar-module'><div class='pillar-label'>PILLAR 03</div><div class='pillar-status'>CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=300, placeholder="Paste your architectural logic or source code for objective audit...")

if st.button("RUN GLOBAL AUDIT"):
    if not payload.strip():
        st.error("ERROR: No data detected.")
    else:
        with st.spinner("Processing structural integrity..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 4. AUDIT RESULTS
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown(f"""
        <div class='result-block'>
            <div class='score-label'>GLOBAL LOGIC SCORE</div>
            <div class='score-val'>{score}%</div>
            <div style='margin-top: 20px;'>
                <span style='background: #111111; color:#ffffff; padding: 4px 10px; font-size: 10px; font-weight:800;'>AUDIT COMPLETE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("SHARE AUTHORITY ON X", f"https://twitter.com/intent/tweet?text=Logic score {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️ Test at AEGIS.", use_container_width=True)

    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.markdown(f"""
            <div class='flaw-alert'>
                <div class='flaw-head'>● FATAL FLAW DETECTED</div>
                <div class='flaw-body'>{f.get('issue')}</div>
                <div style='margin-top: 20px; font-size: 12px; opacity: 0.7;'>IMPACT: {f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # The Cure (Locked Path)
        st.write("")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='cure-locked'>
                    <div style='font-weight:900; letter-spacing:1px;'>REMEDIATION RESTRICTED</div>
                    <div style='color:#666; font-size:12px; margin-top:5px;'>Enterprise pass required to unlock technical solution.</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("SECURE ENTERPRISE PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            passcode = st.text_input("INPUT PASSCODE:", type="password")
            if st.button("UNLOCK SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("Access Denied.")
        else:
            st.markdown(f"""
                <div class='cure-unlocked'>
                    <div style='font-weight:900; color: #238636; margin-bottom: 10px;'>TECHNICAL SOLUTION</div>
                    <code>{f.get('the_cure')}</code>
                </div>
            """, unsafe_allow_html=True)

    if st.button("CLEAR TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#999999; font-size:9px; margin-top:100px; font-weight:700; letter-spacing:2px;'>WAT SYSTEMS | AEGIS v12.5 | INDUSTRIAL AUTHORITY</div>", unsafe_allow_html=True)
