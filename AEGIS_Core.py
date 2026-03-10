import streamlit as st
import json
import requests
import urllib.parse
import time
import re

# ────────────────────────────────────────────────
# 1. NEURAL DESIGN SYSTEM (ULTRA-PREMIUM / UNICORN)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | Neural Singularity",
    layout="centered",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The "Neural Void" High-Fidelity CSS
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

[data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
.stApp { 
    background: radial-gradient(circle at 10% 10%, #0d0d1a 0%, #000000 35%);
    background-color: #000000;
    color: #e8eaed; 
    font-family: 'Inter', sans-serif; 
}
.block-container { padding-top: 5rem !important; max-width: 800px !important; }

/* 1. Brand Identity */
.brand-box { margin-bottom: 50px; text-align: left; animation: fadeIn 1s ease-out; }
.brand-logo {
    font-weight: 800; font-size: 2.6rem; letter-spacing: -1.5px;
    background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    display: inline-block;
}
.brand-meta { font-size: 11px; font-weight: 600; color: #444; letter-spacing: 4px; text-transform: uppercase; margin-top: 10px; }

/* 2. Intelligence Input */
.stTextArea textarea { 
    background-color: rgba(255, 255, 255, 0.02) !important; 
    border: 1px solid rgba(255, 255, 255, 0.08) !important; 
    border-radius: 24px !important; 
    color: #f1f3f4 !important; 
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important; padding: 35px !important; line-height: 1.8;
    min-height: 380px !important; transition: 0.4s all ease;
}
.stTextArea textarea:focus { border-color: #4285F4 !important; background-color: rgba(66, 133, 244, 0.03) !important; }

/* 3. Catalyst Trigger */
div.stButton > button {
    background: linear-gradient(90deg, #4285F4, #9B72CB) !important;
    color: #ffffff !important; font-weight: 700 !important; font-size: 1rem !important;
    border-radius: 100px !important; padding: 14px 60px !important;
    width: auto !important; border: none !important; margin: 25px 0;
    transition: 0.3s all cubic-bezier(0.16, 1, 0.3, 1);
}
div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 10px 40px rgba(155, 114, 203, 0.4); }

/* 4. Reveal Matrix */
.result-card {
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 70px 50px; border-radius: 40px; margin-top: 60px;
}
.score-label { font-size: 13px; font-weight: 800; color: #5f6368; letter-spacing: 3px; text-transform: uppercase; }
.score-val { font-size: 9rem; font-weight: 800; color: #ffffff; line-height: 0.9; margin: 25px 0; letter-spacing: -6px; }

/* 5. Detailed Findings (The Premium Freemium) */
.finding-item { border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 50px 0; margin-top: 40px; }
.f-badge { color: #ff6b6b; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; display: block; }
.f-title { font-size: 2.2rem; font-weight: 700; color: #ffffff; margin-bottom: 20px; line-height: 1.2; letter-spacing: -0.5px; }
.f-desc { font-size: 1.2rem; color: #9aa0a6; line-height: 1.9; }

/* 6. The Cure: 100x Value Blueprint */
.cure-gate {
    background: linear-gradient(180deg, rgba(227, 179, 65, 0.06) 0%, rgba(0,0,0,0) 100%);
    border: 1px solid rgba(227, 179, 65, 0.2);
    padding: 50px; border-radius: 32px; margin-top: 40px;
}
.cure-tag { font-size: 12px; font-weight: 800; color: #e3b341; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 25px; display: block; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
''', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (OPERATIONAL MONITORING)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *AEGIS NEURAL v43* | Score: {score}% | Issues: {issues_count} | 📡 WAT SYSTEMS"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (100X VALUE PROMPT LOGIC)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    
    last_err = ""
    for model in model_pool:
        try:
            # 💎 ULTRA-HIGH VALUE PROMPT: สั่งงานระดับ Senior Architect
            prompt = (
                "You are AEGIS, the supreme Neural Logic Auditor by WAT SYSTEMS. "
                "Dissect the payload for FATAL logic and structural failures. Output JSON ONLY. "
                "For 'the_cure', you MUST provide an exhaustive MASTER-GRADE Blueprint worth thousands of dollars: "
                "1. Root Cause Analysis: Deep dive into WHY this logic fails from a system perspective. "
                "2. Implementation Strategy: Step-by-step technical solution using senior-level clean code. "
                "3. Architectural Prevention: How to refactor the overall system to prevent this class of bug forever. "
                "4. Verification Checklist: How to verify the fix works. "
                "Format: {\"trust_score\": int, \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
            )
            
            payload_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:15000]}"}
                ],
                "temperature": 0.0
            }
            if "gemini" in model: payload_data["response_format"] = {"type": "json_object"}

            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps(payload_data), timeout=55
            )
            
            if resp.status_code == 200:
                raw = resp.json()['choices'][0]['message']['content'].strip()
                # 🛡️ Advanced JSON Recovery: ป้องกันปัญหา 0% จาก Markdown ขยะ
                json_match = re.search(r'\{.*\}', raw, re.DOTALL)
                if json_match: raw = json_match.group(0)
                
                result = json.loads(raw)
                send_radar(result.get('trust_score', 0), len(result.get('findings', [])))
                return result
            last_err = f"API {resp.status_code}: {resp.text}"
        except Exception as e:
            last_err = str(e)
            continue
            
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Verify credits."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown('<div class="brand-box"><h1 class="brand-logo">AEGIS Neural</h1><div class="brand-meta">NEURAL LOGIC AUTHORITY — WAT SYSTEMS</div></div>', unsafe_allow_html=True)

payload = st.text_area("", placeholder="Inject code or architectural DNA for elite neural dissection...")

if st.button("Dissect Logic"):
    if not payload.strip(): st.error("No data detected.")
    else:
        with st.spinner("Analyzing structural DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (ULTRA-VALUE EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>NEURAL INTEGRITY INDEX</div><div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    
    share_msg = f"Neural Logic Scanned: {score}% on AEGIS. Verified by WAT SYSTEMS 🛡️✦"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f'<div><a href="{share_url}" target="_blank" style="color:#8ab4f8; text-decoration:none; font-size:14px; font-weight:600;">𝕏 Broadcast Result to Global Authority</a></div>', unsafe_allow_html=True)

    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f'''
            <div class="finding-item">
                <span class="f-badge">IDENTIFIER_VULN_{i+1:02}</span>
                <div class="f-title">{f.get('issue')}</div>
                <div class="f-desc"><b>CATASTROPHIC IMPACT:</b> {f.get('catastrophic_impact')}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        if not st.session_state.unlocked:
            st.markdown('<div class="cure-gate" style="text-align:center;"><span class="cure-tag">🔒 MASTER BLUEPRINT ENCRYPTED</span><div style="color:#444; font-size:14px;">Enterprise Pass required to access the 100x Value Remediation Blueprint.</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="cure-gate"><span class="cure-tag">💎 MASTER-GRADE TECHNICAL BLUEPRINT</span></div>', unsafe_allow_html=True)
            st.markdown(f.get('the_cure')) # แสดงเป็น Markdown เพื่อความสวยงามของ Blueprint

    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 Secure Sovereign Pass ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        passcode = st.text_input("AUTHORIZE_PASSCODE:", type="password")
        if st.button("UNLOCK MASTER BLUEPRINT"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("AUTHORIZATION DENIED.")

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("New Analysis Session"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown('<div style="text-align:center; color:#222; font-size:10px; margin-top:10rem; padding-bottom:5rem; letter-spacing:6px; font-weight:800;">WAT SYSTEMS | AEGIS v43.0 | NEURAL SINGULARITY</div>', unsafe_allow_html=True)
