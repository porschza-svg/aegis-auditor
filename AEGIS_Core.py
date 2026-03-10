import streamlit as st
import json
import requests
import urllib.parse
import time
import re

# ────────────────────────────────────────────────
# 1. SOVEREIGN DESIGN SYSTEM (FINAL UNICORN GRADE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | Sovereign Authority",
    layout="centered",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Persistence Strategy
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# High-Fidelity "Golden Sovereign" CSS
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* UI Neutralization */
[data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
.stApp { 
    background: radial-gradient(circle at 10% 10%, #0d0d1a 0%, #000000 35%);
    background-color: #000000;
    color: #f1f3f4; 
    font-family: 'Inter', sans-serif; 
}
.block-container { padding-top: 5rem !important; max-width: 850px !important; }

/* 1. Monolithic Brand Identity */
.brand-box { margin-bottom: 60px; text-align: left; animation: fadeIn 1.5s ease-out; }
.brand-logo {
    font-weight: 800; font-size: 2.6rem; letter-spacing: -1.5px;
    background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    display: inline-block;
}
.brand-meta { font-size: 11px; font-weight: 600; color: #444; letter-spacing: 5px; text-transform: uppercase; margin-top: 10px; }

/* 2. Neural Terminal Interface */
.stTextArea textarea { 
    background-color: rgba(255, 255, 255, 0.015) !important; 
    border: 1px solid rgba(255, 255, 255, 0.08) !important; 
    border-radius: 28px !important; 
    color: #ffffff !important; 
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 16px !important; padding: 35px !important; line-height: 1.8;
    min-height: 380px !important; transition: 0.5s all;
}
.stTextArea textarea:focus { border-color: #4285F4 !important; background-color: rgba(66, 133, 244, 0.03) !important; box-shadow: 0 0 50px rgba(66, 133, 244, 0.05) !important; }

/* 3. Executive Trigger Button */
div.stButton > button {
    background: linear-gradient(90deg, #4285F4, #9B72CB) !important;
    color: #ffffff !important; font-weight: 700 !important; font-size: 1.05rem !important;
    border-radius: 100px !important; padding: 16px 60px !important;
    width: auto !important; border: none !important; margin: 25px 0;
    transition: 0.3s all cubic-bezier(0.16, 1, 0.3, 1);
}
div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 10px 40px rgba(155, 114, 203, 0.4); }

/* 4. Authority Reveal Card */
.result-card {
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 70px 50px; border-radius: 40px; margin-top: 60px;
    box-shadow: 0 40px 100px rgba(0,0,0,0.8);
}
.score-label { font-size: 12px; font-weight: 800; color: #5f6368; letter-spacing: 4px; text-transform: uppercase; }
.score-val { font-size: 9rem; font-weight: 800; color: #ffffff; line-height: 0.85; margin: 25px 0; letter-spacing: -6px; }

/* 5. Precision Finding Blocks */
.finding-item { border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 50px 0; margin-top: 40px; }
.f-badge { color: #ff6b6b; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 20px; display: block; }
.f-title { font-size: 2.4rem; font-weight: 700; color: #ffffff; margin-bottom: 20px; line-height: 1.1; letter-spacing: -1.5px; }
.f-desc { font-size: 1.2rem; color: #8b949e; line-height: 1.9; }

/* 6. The Master Blueprint (100x Value) */
.blueprint-card {
    background: linear-gradient(180deg, rgba(227, 179, 65, 0.08) 0%, rgba(0,0,0,0) 100%);
    border: 1px solid rgba(227, 179, 65, 0.3);
    padding: 60px; border-radius: 32px; margin-top: 40px;
}
.blueprint-tag { font-size: 12px; font-weight: 800; color: #e3b341; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 30px; display: block; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
''', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (PERFORMANCE MONITORING)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, latency=0):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = (
                f"🛡️ *AEGIS AUTHORITY DISSECTION*\n\n"
                f"● *INTEGRITY SCORE:* {score}%\n"
                f"● *RISKS IDENTIFIED:* {issues_count}\n"
                f"● *LATENCY:* {latency:.2f}s\n\n"
                f"📡 _Sovereign Operational: WAT SYSTEMS_"
            )
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (ORACLE GRADE PROMPT)
# ────────────────────────────────────────────────
def run_audit(payload):
    start_time = time.time()
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_OFFLINE", "catastrophic_impact": "API Secrets missing.", "the_cure": "Configure API Access."}]}

    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    
    last_err = ""
    for model in model_pool:
        try:
            # 💎 THE ORACLE PROMPT: 100x Value Strategy
            prompt = (
                "You are AEGIS, the Supreme Lead Solutions Architect by WAT SYSTEMS. "
                "Dissect the payload for fatal structural, logic, and architectural failures. "
                "Output JSON ONLY. Format: {\"trust_score\": int, \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                "\n\nFor 'the_cure', provide a MASTER-GRADE Architectural Report: "
                "1. ROOT CAUSE: Analyze the logic failure from a computer science first-principles perspective. "
                "2. STRATEGIC REMEDIATION: Provide clean, high-end code solution. "
                "3. PREVENTATIVE ARCHITECTURE: How to refactor the entire system to immunize it from this vulnerability class. "
                "4. VERIFICATION Protocol: Precise steps to validate the fix."
            )
            
            payload_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"AUDIT_PAYLOAD:\n{payload[:15000]}"}
                ],
                "temperature": 0.0
            }
            if "gemini" in model: payload_data["response_format"] = {"type": "json_object"}

            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps(payload_data), timeout=65
            )
            
            if resp.status_code == 200:
                raw = resp.json()['choices'][0]['message']['content'].strip()
                # 🛡️ Safe JSON Extraction
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if match: raw = match.group(0)
                
                result = json.loads(raw)
                latency = time.time() - start_time
                send_radar(result.get('trust_score', 0), len(result.get('findings', [])), latency)
                return result
            last_err = f"API Error {resp.status_code}: {resp.text}"
        except Exception as e:
            last_err = str(e)
            continue
            
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Check credits or status."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown('<div class="brand-box"><h1 class="brand-logo">AEGIS Neural</h1><div class="brand-meta">NEURAL LOGIC AUTHORITY — WAT SYSTEMS</div></div>', unsafe_allow_html=True)

payload = st.text_area("", placeholder="Inject code or architectural DNA for elite neural dissection...")

if st.button("Dissect Neural Pathways"):
    if not payload.strip(): st.error("NULL_PAYLOAD_DETECTED")
    else:
        with st.spinner("Decoding structural DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (100X VALUE EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>NEURAL INTEGRITY INDEX</div><div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    
    # Premium Viral Integration
    share_msg = f"My logic scored {score}% on AEGIS Neural Auditor. Verified by WAT SYSTEMS 🛡️✦"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f'<div><a href="{share_url}" target="_blank" style="color:#8ab4f8; text-decoration:none; font-size:14px; font-weight:700; border-bottom:1px solid #222; padding-bottom:5px;">𝕏 Broadcast Result to Global Authority</a></div>', unsafe_allow_html=True)

    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f'''
            <div class="finding-item">
                <span class="f-badge">IDENTIFIER_VULN_{i+1:02}</span>
                <div class="f-title">{f.get('issue')}</div>
                <div class="f-desc"><b>ANALYSIS:</b> {f.get('catastrophic_impact')}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        if not st.session_state.unlocked:
            st.markdown('<div class="blueprint-card" style="text-align:center;"><span class="blueprint-tag">🔒 SOVEREIGN BLUEPRINT ENCRYPTED</span><div style="color:#555; font-size:14px; font-weight:500;">SECURE ENTERPRISE PASS TO ACCESS 100X VALUE REMEDIATION.</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="blueprint-card"><span class="blueprint-tag">💎 MASTER-GRADE TECHNICAL BLUEPRINT</span></div>', unsafe_allow_html=True)
            st.markdown(f.get('the_cure'))

    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 SECURE SOVEREIGN PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        passcode = st.text_input("AUTHORIZE_PASSCODE:", type="password")
        if st.button("UNLOCK MASTER BLUEPRINT"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("AUTHORIZATION_DENIED")

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("New Dissection Session", type="secondary"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown('<div style="text-align:center; color:#222; font-size:11px; margin-top:10rem; padding-bottom:5rem; letter-spacing:12px; font-weight:800;">WAT SYSTEMS | AEGIS v45.0 | FINAL AUTHORITY</div>', unsafe_allow_html=True)
