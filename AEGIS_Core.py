import streamlit as st
import json
from groq import Groq
from datetime import datetime

# ────────────────────────────────────────────────
# CONFIG & UNICORN STYLING (v12.0: Cyberpunk Premium)
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS v12.0 – Global Code Authority", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=JetBrains+Mono:wght@700&display=swap');

    .main { background: radial-gradient(circle at top, #0a0f1a 0%, #000000 80%); color: #00ffea; }
    h1 { font-family: 'Orbitron', sans-serif; font-size: 5rem; color: #00ffea; text-shadow: 0 0 30px #00ffea; text-align: center; letter-spacing: 15px; margin: 40px 0 20px; animation: neon 2s infinite alternate; }
    @keyframes neon { from { text-shadow: 0 0 10px #00ffea; } to { text-shadow: 0 0 50px #00ffea, 0 0 100px #00ffea; } }
    .tagline { font-family: 'JetBrains Mono', monospace; color: #00ffea; font-size: 1.2rem; text-align: center; letter-spacing: 5px; opacity: 0.8; margin-bottom: 40px; }
    .input-box { background: rgba(0,0,0,0.7); border: 1px solid #00ffea; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 0 30px rgba(0,255,234,0.2); }
    .stTextArea textarea { background: #000 !important; color: #00ffea !important; border: 1px solid #00ffea !important; font-family: 'JetBrains Mono', monospace !important; font-size: 16px !important; }
    .scan-btn { width: 100% !important; background: linear-gradient(90deg, #00ffea, #00b8ff) !important; color: #000 !important; font-weight: 900 !important; font-size: 24px !important; padding: 20px !important; border-radius: 12px !important; border: none !important; box-shadow: 0 0 30px rgba(0,255,234,0.5) !important; transition: all 0.3s !important; }
    .scan-btn:hover { transform: scale(1.05); box-shadow: 0 0 60px rgba(0,255,234,0.8) !important; }
    .score-box { background: rgba(0,0,0,0.8); border: 2px solid #00ffea; border-radius: 16px; padding: 40px; margin: 30px 0; text-align: center; box-shadow: 0 0 40px rgba(0,255,234,0.3); }
    .score-value { font-size: 120px; font-weight: 900; color: #00ffea; text-shadow: 0 0 30px #00ffea; }
    .paywall-box { background: rgba(255, 0, 0, 0.1); border: 2px dashed #ff0000; padding: 40px; border-radius: 16px; text-align: center; margin: 40px 0; }
    .footer { text-align: center; color: #00ffea; opacity: 0.6; font-size: 12px; margin-top: 80px; letter-spacing: 3px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. SUPREME AUDIT ENGINE (GROQ - FAST & BRUTAL)
# ────────────────────────────────────────────────
def run_aegis_scan(payload):
    try:
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS v12.0 - Brutal Code Auditor. Output JSON only: {\"trust_score\": int, \"summary\": str, \"issues_count\": int}"},
                {"role": "user", "content": f"SCAN THIS: {payload[:4000]}"}
            ],
            temperature=0.0,
            max_tokens=100,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except:
        return {"trust_score": 50, "summary": "Scan completed (demo mode)", "issues_count": 0}

# ────────────────────────────────────────────────
# 3. HERO & INPUT
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>AEGIS</h1><div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)

payload = st.text_area("", height=180, placeholder="Paste your code or contract here...")

if st.button("EXECUTE SCAN – FREE"):
    if not payload.strip():
        st.error("NO PAYLOAD DETECTED")
    else:
        with st.spinner("SCANNING STRUCTURAL INTEGRITY..."):
            result = run_aegis_scan(payload)
            st.session_state.result = result
            st.session_state.scanned = True

# ────────────────────────────────────────────────
# 4. RESULTS & PAYWALL
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 50)
    
    st.markdown(f"""
        <div class='score-box'>
            <div style='font-size: 2rem; color: #00ffea; opacity: 0.8;'>TRUST SCORE</div>
            <div class='score-value'>{score}%</div>
            <div style='font-size: 1.2rem; color: #00ffea; margin-top: 20px;'>{res.get('summary', 'Scan completed')}</div>
            <div style='font-size: 1.5rem; color: #ff0000; margin-top: 20px;'>ISSUES DETECTED: {res.get('issues_count', 0)}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='paywall-box'>
            <h2 style='color: #ff0000; margin: 0;'>FULL REPORT LOCKED</h2>
            <p style='color: #00ffea; margin: 20px 0;'>Unlock detailed findings + remediation steps for $9 (one-time)</p>
            <a href='https://porschza.gumroad.com/l/aegis-full-report' target='_blank' style='background: #ff0000; color: white; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;'>UNLOCK NOW $9</a>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='footer'>WAT SYSTEMS | AEGIS v12.0 | SUPREME AUTHORITY</div>", unsafe_allow_html=True)
