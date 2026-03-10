import streamlit as st
import json
import requests
import anthropic
import urllib.parse

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI CONFIG & NEURAL STYLING
# ────────────────────────────────────────────────
st.set_page_config(page_title="WAT SYSTEMS | AEGIS Global Authority", layout="centered", page_icon="🛡️")

if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

st.markdown("""
    <style>
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .hero-container { text-align: center; padding: 40px 0 10px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 12px; font-weight: 900; margin-bottom: 5px; text-shadow: 0 0 50px rgba(88, 166, 255, 0.4); font-size: 3rem; }
    .brand-tag { color: #58a6ff; font-size: 12px; letter-spacing: 5px; font-weight: 800; margin-bottom: 40px; text-transform: uppercase; }
    .score-display { background: #0d1117; padding: 40px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 30px 0; border-top: 5px solid #58a6ff; }
    .good-card { background: rgba(46, 160, 67, 0.08); border-left: 4px solid #2ea043; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .flaw-card { background: rgba(248, 81, 73, 0.08); border-left: 4px solid #f85149; padding: 25px; border-radius: 8px; margin-bottom: 25px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .locked-cure-box { background: repeating-linear-gradient( 45deg, rgba(227, 179, 65, 0.03), rgba(227, 179, 65, 0.03) 10px, rgba(0,0,0,0) 10px, rgba(0,0,0,0) 20px ); border: 1px dashed #e3b341; padding: 40px; border-radius: 16px; text-align: center; margin-bottom: 20px; }
    .unlocked-cure { background: rgba(46, 160, 67, 0.1); border: 1px solid #2ea043; padding: 30px; border-radius: 16px; color: #e6edf3; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. SUPREME AUDIT ENGINE (CLAUDE 3.5 SONNET)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key: raise Exception("Missing ANTHROPIC_API_KEY in Secrets.")
        
        client = anthropic.Anthropic(api_key=api_key)
        system_prompt = (
            "You are AEGIS, a brutal, elite Universal Logic Auditor by WAT SYSTEMS. "
            "Analyze the payload strictly. Output JSON ONLY format: "
            "{"
            "  \"trust_score\": int (0-100), \"strengths\": [\"str\"], "
            "  \"findings\": [{\"issue\": \"str\", \"severity\": \"Critical\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}] "
            "}"
            "Respond ONLY with valid JSON."
        )
        
        message = client.messages.create(
            model="claude-3-5-sonnet-latest", max_tokens=2500, temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": f"PAYLOAD:\n{payload[:12000]}"}]
        )
        
        raw_content = message.content[0].text.strip()
        if "
