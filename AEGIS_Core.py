import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI CONFIG & NEURAL STYLING
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="WAT SYSTEMS | AEGIS Global Authority", 
    layout="centered", 
    page_icon="🛡️"
)

# Initialize Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

st.markdown("""
    <style>
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .hero-container { text-align: center; padding: 40px 0 10px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 12px; font-weight: 900; margin-bottom: 5px; text-shadow: 0 0 50px rgba(88, 166, 255, 0.4); font-size: 3rem; }
    .brand-tag { color: #58a6ff; font-size: 11px; letter-spacing: 5px; font-weight: 800; margin-bottom: 40px; text-transform: uppercase; opacity: 0.8; }
    .score-display { background: #0d1117; padding: 45px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 30px 0; border-top: 6px solid #58a6ff; }
    .good-card { background: rgba(46, 160, 67, 0.08); border-left: 4px solid #2ea043; padding: 22px; border-radius: 10px; margin-bottom: 18px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .flaw-card { background: rgba(248, 81, 73, 0.08); border-left: 4px solid #f85149; padding: 28px; border-radius: 10px; margin-bottom: 30px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .locked-cure-box { background: repeating-linear-gradient( 45deg, rgba(227, 179, 65, 0.04), rgba(227, 179, 65, 0.04) 10px, rgba(0,0,0,0) 10px, rgba(0,0,0,0) 20px ); border: 2px dashed #e3b341; padding: 45px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    .unlocked-cure { background: rgba(46, 160, 67, 0.12); border: 1px solid #2ea043; padding: 35px; border-radius: 16px; color: #e6edf3; }
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; color: #e6edf3 !important; font-family: 'Fira Code', monospace; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. OPENROUTER FREE ENGINE (ZERO-COST AUDIT)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        # ดึง Key จาก Secrets ถ้ามี ถ้าไม่มีให้หยุดและแจ้งเตือน
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {
                "trust_score": 0, "strengths": [], 
                "findings": [{
                    "issue": "Missing System Secrets", "severity": "Critical", 
                    "catastrophic_impact": "The auditor is blind. No API key found in Streamlit Secrets.", 
                    "the_cure": "Go to Streamlit Dashboard -> Settings -> Secrets and add: ANTHROPIC_API_KEY = 'your_key_here'"
                }]
            }
        
        # ใช้ Free Model ที่ฉลาดที่สุดในปัจจุบัน (Llama 3.1 8B Free)
        # ไม่ต้องใช้เงินเติมเครดิตใน OpenRouter เพื่อรันตัวนี้
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://aegis-auditor.streamlit.app",
            "X-Title": "AEGIS Authority",
        }
        data = {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are AEGIS, a brutal Logic Auditor. Output JSON ONLY format: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"severity\": \"Critical\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                {"role": "user", "content": f"PAYLOAD:\n{payload[:8000]}"}
            ],
            "temperature": 0.1
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if 'choices' not in result:
            raise Exception(result.get('error', {}).get('message', 'API connection failed.'))
            
        raw_content = result['choices'][0]['message']['content'].strip()
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_content)
    except Exception as e:
        return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Uplink Error", "severity": "Critical", "catastrophic_impact": str(e), "the_cure": "Check your OpenRouter API Key in Secrets."}]}

# ────────────────────────────────────────────────
# 3. UI ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>AEGIS</h1><div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align:center; color:#238636; font-size:10px; font-weight:800; letter-spacing:3px; margin-bottom:40px;'>
        ● SYSTEM STATUS: ONLINE | ENGINE: FREE-TIER ACTIVE
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1: st.info("💻 CODE SECURITY")
with col2: st.info("🤖 WORKFLOW LOGIC")
with col3: st.info("🔗 SMART CONTRACTS")

st.write("")
payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste your logic here for audit...")

if st.button("🚀 INITIATE GLOBAL SCAN (FREE)"):
    if not payload.strip():
        st.error("❌ ERROR: No payload detected.")
    else:
        with st.spinner("Decoding structural truth..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 4. RESULTS
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    st.markdown("---")
    
    st.markdown(f"""
        <div class='score-display'>
            <h3>GLOBAL TRUST SCORE</h3>
            <h1 style='font-size: 85px; color:#58a6ff; margin:0;'>{score}%</h1>
            <p style='color:#8b949e; letter-spacing:2px;'>Universal Logic Standard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Strengths
    strengths = res.get("strengths", [])
    if strengths:
        st.subheader("✅ ARCHITECTURAL STRENGTHS")
        for s in strengths:
            st.markdown(f"<div class='good-card'><b>ANALYSIS:</b> {s}</div>", unsafe_allow_html=True)

    # Fatal Flaw
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.subheader("🚨 THE FATAL FLAW")
        st.markdown(f"""
            <div class='flaw-card'>
                <h4 style='color:#f85149; margin-top:0;'>⚠️ {f.get('issue')}</h4>
                <h5 style='color:#ff7b72; margin-top:15px;'>💥 CATASTROPHIC IMPACT:</h5>
                <p><i>"{f.get('catastrophic_impact')}"</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall
        st.subheader("🧬 THE SINGLE PATH (REMEDIATION)")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='locked-cure-box'>
                    <h3 style='margin:0; color:#e3b341;'>🔒 THE CURE IS ENCRYPTED</h3>
                    <p style='color:#8b949e; margin-top:10px;'>Full remediation code is restricted to Enterprise Access.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.link_button("👉 SECURE ENTERPRISE PASS ($9) TO UNLOCK", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            st.write("")
            passcode = st.text_input("ENTER PASSCODE:", type="password")
            if st.button("🔓 VERIFY & UNLOCK"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("❌ Invalid Passcode.")
        else:
            st.success("✅ ACCESS GRANTED")
            st.markdown(f"<div class='unlocked-cure'><h3>🟢 TECHNICAL SOLUTION</h3><p style='font-family: \"Fira Code\", monospace;'>{f.get('the_cure')}</p></div>", unsafe_allow_html=True)

    if st.button("🔄 CLEAR SCAN"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#484f58; font-size:10px; margin-top:100px; letter-spacing:2px;'>POWERED BY WAT SYSTEMS | AEGIS v11.7</div>", unsafe_allow_html=True)
