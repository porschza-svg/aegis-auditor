import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. NEURAL DESIGN SYSTEM (GEMINI ELITE GRADE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | Neural Logic Authority",
    layout="centered",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Initialize Core States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The Gemini "Neural Monolith" CSS (Premium Experience)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Authority Background */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .stApp { 
        background: radial-gradient(circle at 20% 20%, #0d0d1a 0%, #000000 40%);
        background-color: #000000;
        color: #e8eaed; 
        font-family: 'Inter', sans-serif; 
    }
    .block-container { padding-top: 5rem !important; max-width: 800px !important; }

    /* 1. Brand Signature: Gemini Intelligence Style */
    .brand-box { margin-bottom: 60px; text-align: left; }
    .brand-logo {
        font-weight: 600;
        font-size: 2.2rem;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .brand-sparkle { color: #8ab4f8; font-size: 1.2rem; vertical-align: super; margin-left: 5px; opacity: 0.8; }
    .brand-meta { font-size: 10px; font-weight: 500; color: #5f6368; letter-spacing: 3px; text-transform: uppercase; margin-top: 8px; }

    /* 2. Intelligence Terminal (Neural Input) */
    .stTextArea textarea { 
        background-color: #0d0d0d !important; 
        border: 1px solid #202124 !important; 
        border-radius: 24px !important; 
        color: #f1f3f4 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 30px !important;
        line-height: 1.8;
        min-height: 320px !important;
        transition: 0.4s all ease;
    }
    .stTextArea textarea:focus { border-color: #8ab4f8 !important; background-color: #111 !important; box-shadow: 0 0 25px rgba(66, 133, 244, 0.1) !important; }

    /* 3. Catalyst Trigger (Neural Pill) */
    div.stButton > button {
        background: linear-gradient(90deg, #4285F4, #9B72CB) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        border-radius: 100px !important;
        padding: 12px 40px !important;
        width: auto !important;
        border: none !important;
        transition: 0.3s all cubic-bezier(0.16, 1, 0.3, 1);
        margin-top: 20px;
    }
    div.stButton > button:hover { transform: scale(1.03); box-shadow: 0 10px 30px rgba(155, 114, 203, 0.3); }

    /* 4. The Reveal: Logic Integrity Dashboard */
    .result-aura {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 60px 40px;
        border-radius: 32px;
        margin-top: 60px;
    }
    .score-label { font-size: 0.9rem; color: #9aa0a6; letter-spacing: 1px; margin-bottom: 5px; }
    .score-val { font-size: 7rem; font-weight: 700; color: #ffffff; line-height: 1; margin: 0; letter-spacing: -4px; }
    .badge-ai { background: rgba(138, 180, 248, 0.08); color: #8ab4f8; padding: 6px 16px; border-radius: 100px; font-size: 11px; font-weight: 500; margin-top: 25px; display: inline-block; }

    /* 5. Vulnerability Dissection (Premium Freemium) */
    .finding-block { border-top: 1px solid #202124; padding: 40px 0; margin-top: 40px; }
    .f-header { color: #f28b82; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; display: block; }
    .f-title { font-size: 1.8rem; font-weight: 600; color: #ffffff; margin-bottom: 15px; line-height: 1.3; }
    .f-impact { font-size: 1.1rem; color: #9aa0a6; line-height: 1.8; }

    /* 6. The Restricted Chamber (Paywall) */
    .locked-chamber {
        background: #0a0a0a;
        border: 1px dashed #3c4043;
        padding: 50px;
        border-radius: 24px;
        text-align: center;
        margin-top: 30px;
    }
    .locked-tag { font-size: 11px; font-weight: 700; color: #fdd663; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 20px; display: block; }

    /* X Share Integration */
    .x-btn { 
        display: inline-block; 
        color: #ffffff !important; 
        padding: 12px 30px; 
        border-radius: 100px; 
        text-decoration: none; 
        font-weight: 500; 
        font-size: 0.9rem;
        background: #111;
        border: 1px solid #3c4043;
        transition: 0.3s;
        margin-top: 30px;
    }
    .x-btn:hover { background: #fff; color: #000 !important; }

    .footer { text-align: center; color: #3c4043; font-size: 0.8rem; margin-top: 12rem; padding-bottom: 4rem; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (RESILIENT UPLINK)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS NEURAL* | Score: {score}% | Issues: {issues_count} | 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (ZERO-FAILURE ROUTING)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_OFFLINE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    
    last_err = ""
    for model in model_pool:
        try:
            payload_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are AEGIS, the supreme Logic Auditor. Analyze strictly for structural failures. Output valid JSON ONLY. Template: {\"trust_score\": int, \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                    {"role": "user", "content": f"AUDIT_PAYLOAD:\n{payload[:15000]}"}
                ],
                "temperature": 0.0
            }
            if "gemini" in model: payload_data["response_format"] = {"type": "json_object"}

            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps(payload_data), 
                timeout=50
            )
            
            if resp.status_code == 200:
                raw_json = resp.json()['choices'][0]['message']['content'].strip()
                # Clean potential markdown wrapping
                if raw_json.startswith("```"):
                    raw_json = raw_json.split("```")[1]
                    if raw_json.startswith("json"): raw_json = raw_json[4:]
                    raw_json = raw_json.strip()
                
                result = json.loads(raw_json)
                send_radar(result.get('trust_score', 0), len(result.get('findings', [])))
                return result
            
            last_err = f"API {resp.status_code}: {resp.text}"
        except Exception as e:
            last_err = str(e)
            continue
            
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Check credits or status."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE (GEMINI STYLE)
# ────────────────────────────────────────────────
st.markdown("""
    <div class="brand-box">
        <h1 class="brand-logo">AEGIS Neural <span class="brand-sparkle">✦</span></h1>
        <div class="brand-meta">NEURAL LOGIC AUTHORITY — WAT SYSTEMS</div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("", placeholder="How can AEGIS dissect your logic today? Paste architectural spec or code...")

if st.button("Dissect Logic"):
    if not payload.strip(): st.error("No data detected.")
    else:
        with st.spinner("Analyzing neural pathways..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (PLUGIN EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>NEURAL TRUST INDEX</div><div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div class='badge-ai'>Analysis Authenticated by AEGIS v41.0 Neural Core</div>", unsafe_allow_html=True)
    
    share_msg = f"My project logic scored {score}% on AEGIS Neural Auditor. Verified by WAT SYSTEMS 🛡️✦"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div><a href='{share_url}' target='_blank' class='x-btn'>Broadcast Authority on 𝕏</a></div>", unsafe_allow_html=True)

    st.write("")
    findings = res.get("findings", [])
    for i, f in enumerate(findings):
        st.markdown(f"""
            <div class="finding-block">
                <span class="f-header">VULNERABILITY_ID_{i+1:02}</span>
                <div class="f-title">{f.get('issue')}</div>
                <div class="f-impact"><b>DETAILED IMPACT:</b> {f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.unlocked:
            st.markdown("""
                <div class="locked-chamber">
                    <span class="locked-tag">🔒 REMEDIATION ENCRYPTED</span>
                    <div style="color:#5f6368; font-size:1rem; margin-bottom:20px;">Secure Enterprise Pass to decrypt the technical solution.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**TECHNICAL SOLUTION:**")
            st.code(f.get('the_cure'), language='python')

    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 Secure Enterprise Pass ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("Enter Passcode Authorization:", type="password")
        if st.button("UNLOCK REMEDIATION"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS DENIED.")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("New Dissection Session", type="secondary"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div class='footer'>WAT SYSTEMS | AEGIS v41.0 | NEURAL MONOLITH</div>", unsafe_allow_html=True)
