import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. OBELISK DESIGN SYSTEM (BILLION DOLLAR UNICORN)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS NEURAL | AUTHORITY",
    layout="centered",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Persistence Strategy
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "Absolute Authority" CSS Framework
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Core Neutralization */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 6rem !important; max-width: 850px !important; }

    /* 1. Brand Header: Monolithic Signature */
    .header-box { text-align: left; margin-bottom: 70px; border-left: 2px solid #30363d; padding-left: 30px; }
    .logo-main {
        font-weight: 900;
        font-size: 3rem;
        letter-spacing: -3px;
        background: linear-gradient(180deg, #FFFFFF 0%, #666666 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }
    .logo-meta { font-size: 10px; font-weight: 700; color: #4285F4; letter-spacing: 5px; text-transform: uppercase; margin-top: 15px; }

    /* 2. Neural Terminal Interface */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 0px !important; 
        color: #e0e0e0 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 40px !important;
        line-height: 1.8;
        min-height: 380px !important;
        box-shadow: inset 0 0 40px rgba(0,0,0,1) !important;
    }
    .stTextArea textarea:focus { border-color: #4285F4 !important; }

    /* 3. Catalyst Trigger (High-End Pill) */
    div.stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 100px !important;
        padding: 16px 50px !important;
        width: auto !important;
        border: none !important;
        margin: 30px 0;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s all cubic-bezier(0.16, 1, 0.3, 1);
    }
    div.stButton > button:hover { 
        background: #4285F4 !important; 
        color: white !important; 
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(66, 133, 244, 0.3);
    }

    /* 4. The Reveal: Neural integrity Wall */
    .result-aura {
        background: #000000;
        border: 1px solid #111111;
        padding: 80px 60px;
        margin-top: 80px;
        position: relative;
    }
    .result-aura::before {
        content: ""; position: absolute; top: -1px; left: -1px; width: 60px; height: 60px;
        border-top: 2px solid #4285F4; border-left: 2px solid #4285F4;
    }
    .score-label { font-size: 11px; font-weight: 800; color: #4b5563; letter-spacing: 5px; text-transform: uppercase; }
    .score-hero { font-size: 10rem; font-weight: 900; color: #ffffff; letter-spacing: -10px; line-height: 0.9; margin: 20px 0; }
    .auth-badge { background: #111111; color: #4285F4; padding: 6px 18px; font-size: 10px; font-weight: 800; letter-spacing: 2px; border: 1px solid #222; }

    /* 5. Risk Architecture */
    .finding-block { border-top: 1px solid #111111; padding: 50px 0; margin-top: 50px; }
    .f-id { color: #ff4b4b; font-size: 9px; font-weight: 900; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; display: block; }
    .f-title { font-size: 2.2rem; font-weight: 700; color: #ffffff; margin-bottom: 20px; line-height: 1.1; letter-spacing: -1px; }
    .f-desc { font-size: 1.2rem; color: #6b7280; line-height: 1.8; }

    /* 6. Paywall: Sovereign Gate */
    .locked-gate {
        background: #030303;
        border: 1px solid #1a1a1a;
        padding: 60px;
        text-align: center;
        margin-top: 40px;
    }
    .gate-label { font-size: 10px; font-weight: 800; color: #e3b341; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 25px; display: block; }

    /* X Integration */
    .share-link { 
        display: inline-block; 
        color: #8b949e !important; 
        text-decoration: none; 
        font-weight: 600; 
        font-size: 13px;
        border-bottom: 1px solid #222;
        padding-bottom: 5px;
        transition: 0.3s;
        margin-top: 40px;
    }
    .share-link:hover { color: #ffffff; border-color: #4285F4; }

    .footer-text { text-align: center; color: #222; font-size: 10px; margin-top: 12rem; padding-bottom: 5rem; font-weight: 800; letter-spacing: 8px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (RE-ENGINEERED)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS NEURAL* | Score: {score}% | Risks: {issues_count} | 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. NEURAL ENGINE (MULTI-MODEL RESILIENCE)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_OFFLINE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    # เลิกใช้รุ่น :free ที่มักเกิด 404 ใช้ Endpoint หลักที่เสถียรกว่า
    model_pool = [
        "google/gemini-2.0-flash-001",
        "google/gemini-flash-1.5",
        "meta-llama/llama-3.3-70b-instruct"
    ]
    
    last_err = ""
    for model in model_pool:
        try:
            payload_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are AEGIS, the elite Logic Auditor. Dissect for ALL logic flaws. Output valid JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                    {"role": "user", "content": f"PAYLOAD:\n{payload[:12000]}"}
                ],
                "temperature": 0.0
            }
            # Only apply response_format for Gemini
            if "gemini" in model: payload_data["response_format"] = {"type": "json_object"}

            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps(payload_data), 
                timeout=50
            )
            
            if resp.status_code == 200:
                raw_json = resp.json()['choices'][0]['message']['content'].strip()
                # Clean markdown backticks if any
                if "
