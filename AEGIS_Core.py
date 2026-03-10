import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. NEURAL MONOLITH UI (GEMINI ENTERPRISE GRADE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS NEURAL | WAT SYSTEMS",
    layout="centered",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Global Session Management
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "Absolute Gemini" Design Language
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Reset */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { 
        background-color: #080808; 
        color: #e3e3e3; 
        font-family: 'Google Sans', sans-serif; 
    }
    .block-container { padding-top: 5rem !important; max-width: 850px !important; }

    /* 1. Header: The Neural Signature */
    .header-box { text-align: left; margin-bottom: 60px; position: relative; }
    .logo-text {
        font-weight: 500;
        font-size: 2.8rem;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .logo-spark { position: absolute; top: -10px; left: 160px; color: #8ab4f8; font-size: 1.5rem; }
    .brand-meta { font-size: 11px; font-weight: 500; color: #80868b; letter-spacing: 3px; text-transform: uppercase; margin-top: 8px; }

    /* 2. Neural Intake Terminal */
    .stTextArea textarea { 
        background-color: #111111 !important; 
        border: 1px solid #2c2c2c !important; 
        border-radius: 28px !important; 
        color: #f1f3f4 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 16px !important;
        padding: 35px !important;
        line-height: 1.7;
        min-height: 350px !important;
        transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTextArea textarea:focus { border-color: #8ab4f8 !important; background-color: #161616 !important; box-shadow: 0 0 30px rgba(66, 133, 244, 0.05) !important; }

    /* 3. Execution Catalyst (Fluid Pill) */
    div.stButton > button {
        background: linear-gradient(90deg, #4285F4, #9B72CB) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        border-radius: 100px !important;
        padding: 14px 45px !important;
        width: auto !important;
        border: none !important;
        margin: 20px 0;
        transition: 0.3s all;
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 8px 30px rgba(155, 114, 203, 0.3); }

    /* 4. The Reveal Wall: Neural Integrity */
    .result-aura {
        background: #111111;
        border: 1px solid #2c2c2c;
        padding: 60px 50px;
        border-radius: 32px;
        margin-top: 60px;
        animation: fadeIn 0.8s ease-out;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    
    .score-label { font-size: 0.95rem; color: #9aa0a6; letter-spacing: 1px; margin-bottom: 10px; }
    .score-hero { font-size: 7.5rem; font-weight: 700; color: #ffffff; letter-spacing: -5px; line-height: 1; margin: 0; }
    .badge-certified { background: rgba(138, 180, 248, 0.08); color: #8ab4f8; padding: 6px 16px; border-radius: 100px; font-size: 12px; font-weight: 500; margin-top: 25px; display: inline-block; }

    /* 5. Detailed Dissection Cards */
    .finding-block { border-top: 1px solid #2c2c2c; padding: 40px 0; margin-top: 40px; }
    .f-tag { color: #f28b82; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; margin-bottom: 15px; display: block; }
    .f-title { font-size: 2rem; font-weight: 500; color: #ffffff; margin-bottom: 15px; line-height: 1.2; }
    .f-desc { font-size: 1.15rem; color: #9aa0a6; line-height: 1.8; }

    /* 6. Paywall: Neural Restriction */
    .locked-chamber {
        background: #0d0d0d;
        border: 1px solid #332b00;
        padding: 50px;
        border-radius: 24px;
        text-align: center;
        margin-top: 30px;
    }
    .locked-label { font-size: 11px; font-weight: 700; color: #fdd663; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 20px; display: block; }

    /* Social Integration */
    .x-share-btn { 
        display: inline-block; 
        color: #ffffff !important; 
        padding: 12px 30px; 
        border-radius: 100px; 
        text-decoration: none; 
        font-weight: 500; 
        font-size: 0.95rem;
        background: #111;
        border: 1px solid #2c2c2c;
        transition: 0.3s;
    }
    .x-share-btn:hover { background: #fff; color: #000 !important; }

    .footer { text-align: center; color: #444; font-size: 0.85rem; margin-top: 10rem; padding-bottom: 4rem; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (RESILIENT)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS NEURAL* | Score: {score}% | Issues: {issues_count} | 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# 3. NEURAL ENGINE (ULTRA-STABLE FALLBACK)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    # ใช้รายชื่อโมเดลที่เสถียรที่สุดในวินาทีนี้ และเอา :free ออกในตัวแรกรองเพื่อความรวดเร็ว
    model_pool = [
        "google/gemini-2.0-flash-001", 
        "google/gemini-flash-1.5", 
        "meta-llama/llama-3.3-70b-instruct"
    ]
    
    last_err = ""
    for model in model_pool:
        try:
            # 🚨 FIX: ไม่ส่ง response_format ถ้าไม่ใช่โมเดลที่มั่นใจ เพื่อเลี่ยง Error 400
            payload_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are AEGIS, the elite Logic Auditor. Analyze for ALL critical flaws. Output valid JSON ONLY. Template: {\"trust_score\": int, \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                    {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:15000]}"}
                ],
                "temperature": 0.0
            }
            
            # ส่งเฉพาะโมเดลที่รองรับ JSON mode แน่นอน
            if "gemini" in model:
                payload_data["response_format"] = {"type": "json_object"}

            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps(payload_data), 
                timeout=45
            )
            
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content'].strip()
                # Clean markdown if AI returns it
                if content.startswith("
