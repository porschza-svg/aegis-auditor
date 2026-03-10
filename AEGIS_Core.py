import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI ARCHITECTURE & HIGH-FIDELITY STYLING
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
    /* Absolute UI Authority */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #05070a; color: #e6edf3; font-family: 'Inter', sans-serif; }
    
    /* Hero Section */
    .hero-container { text-align: center; padding: 60px 0 30px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 18px; font-weight: 900; margin-bottom: 8px; text-shadow: 0 0 40px rgba(88, 166, 255, 0.3); font-size: 4rem; }
    .brand-tag { color: #58a6ff; font-size: 10px; letter-spacing: 6px; font-weight: 800; margin-bottom: 60px; text-transform: uppercase; opacity: 0.6; }
    
    /* System Status Glow */
    .status-indicator { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 50px; background: rgba(35, 134, 54, 0.1); border: 1px solid rgba(46, 160, 67, 0.3); color: #3fb950; font-size: 10px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 40px; }
    
    /* High-Fidelity Matrix Cards (Pillars) */
    .pillar-card { background: #0d1117; border: 1px solid #30363d; padding: 25px; border-radius: 16px; text-align: center; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); border-bottom: 4px solid #30363d; }
    .pillar-card:hover { border-color: #58a6ff; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-bottom-color: #58a6ff; }
    .pillar-icon { font-size: 24px; margin-bottom: 12px; display: block; }
    .pillar-title { font-weight: 900; font-size: 13px; letter-spacing: 1px; color: #ffffff; display: block; margin-bottom: 5px; }
    .pillar-desc { font-size: 10px; color: #8b949e; line-height: 1.4; }

    /* Result Displays */
    .score-container { background: radial-gradient(circle at center, #0d1117 0%, #05070a 100%); padding: 60px; border-radius: 30px; border: 1px solid #30363d; text-align: center; margin: 40px 0; border-top: 2px solid #58a6ff; box-shadow: 0 30px 60px rgba(0,0,0,0.6); }
    .score-value { font-size: 100px; font-weight: 900; color: #ffffff; margin: 0; line-height: 1; text-shadow: 0 0 30px rgba(88, 166, 255, 0.5); }
    
    /* Dangerous Flaw Card */
    .flaw-box { background: rgba(248, 81, 73, 0.05); border: 1px solid rgba(248, 81, 73, 0.2); border-left: 6px solid #f85149; padding: 35px; border-radius: 12px; margin: 30px 0; }
    .flaw-title { color: #f85149; font-weight: 900; font-size: 18px; letter-spacing: 1px; margin-bottom: 15px; text-transform: uppercase; }
    .flaw-impact { color: #e6edf3; font-style: italic; line-height: 1.6; font-size: 16px; }

    /* The Locked Cure - Ultra Premium */
    .locked-zone { background: #010409; border: 2px dashed #e3b341; padding: 50px; border-radius: 20px; text-align: center; margin-top: 40px; }
    .locked-badge { background: #e3b341; color: #000; padding: 5px 15px; border-radius: 4px; font-weight: 900; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; display: inline-block; }
    
    /* Text Area Override */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; font-family: 'Fira Code', monospace; padding: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. LOGIC ENGINE (FREE-TIER OPTIMIZED)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Uplink Failure", "severity": "Critical", "catastrophic_impact": "System Secrets missing. Logic authority compromised.", "the_cure": "Go to Streamlit Settings -> Secrets."}]}
        
        # Using Llama 3.1 8B (Free) for instant execution
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://aegis-auditor.streamlit.app",
                "X-Title": "AEGIS Authority",
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are AEGIS, a brutal Logic Auditor. Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"severity\": \"Critical\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                    {"role": "user", "content": f"PAYLOAD:\n{payload[:10000]}"}
                ],
                "temperature": 0.1
            })
        )
        
        result = response.json()
        raw_content = result['choices'][0]['message']['content'].strip()
        if "
