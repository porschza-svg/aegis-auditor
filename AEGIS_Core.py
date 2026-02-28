import streamlit as st
import json
import time
import io
from groq import Groq

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI CONFIG & NEURAL STYLING
# ────────────────────────────────────────────────
st.set_page_config(page_title="WAT SYSTEMS | AEGIS Global Authority", layout="centered", page_icon="🛡️")

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
    .brand-tag { color: #58a6ff; font-size: 12px; letter-spacing: 5px; font-weight: 800; margin-bottom: 40px; text-transform: uppercase; }
    .uplink-box { background: rgba(31, 111, 235, 0.05); border: 1px dashed #388bfd; border-radius: 16px; padding: 20px; margin-bottom: 25px; text-align: center; }
    div[data-testid="stExpander"] { background: rgba(22, 27, 34, 0.5); border: 1px solid #30363d !important; border-radius: 12px !important; }
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; font-family: 'Fira Code', monospace; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-weight: 900; padding: 18px; border-radius: 12px; border: none; letter-spacing: 2px; }
    .score-display { background: #0d1117; padding: 40px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 30px 0; border-top: 5px solid #58a6ff; }
    .locked-card { background: rgba(227, 179, 65, 0.08); border: 1px dashed #e3b341; padding: 30px; border-radius: 16px; text-align: center; color: #e3b341; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. AUDIT ENGINE (ROBUST VERSION)
# ────────────────────────────────────────────────
def run_aegis_audit(payload, audio_meta=None):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        audio_context = f" [AUDIO_UPLINK_METADATA: {audio_meta}]" if audio_meta else ""
        
        system_prompt = (
            "You are AEGIS, the Supreme Universal Auditor by WAT SYSTEMS. "
            "Detect 3 critical logic flaws. For Code/Business: Focus on structural integrity. "
            "For Music: Analyze structural integrity (Intro/Verse/Chorus balance) and emotional arc logic. "
            "Output JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"PAYLOAD: {payload[:12000]}{audio_context}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        # Clean JSON in case of formatting artifacts
        raw_content = response.choices[0].message.content.strip()
        return json.loads(raw_content)
    except Exception as e: 
        return {"trust_score": 0, "findings": [{"issue": "Uplink Error.", "severity": "Critical", "remediation": f"Verify System Key. (Internal: {str(e)})"}]}

# ────────────────────────────────────────────────
# 3. DASHBOARD ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>AEGIS</h1><div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)
st.markdown("<div style
