import streamlit as st
import json
import requests
import urllib.parse
import time
import re

# ────────────────────────────────────────────────
# 1. SOVEREIGN DESIGN SYSTEM (FULL SPECTRUM UNICORN)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | Neural Authority",
    layout="centered",
    page_icon="🛡️",
    initial_sidebar_state="collapsed"
)

# Persistence Control
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# High-Fidelity "Neural Void" CSS (Billion-Dollar Standard)
st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

[data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
.stApp { 
    background: radial-gradient(circle at 15% 15%, #0d0d1a 0%, #000000 40%);
    background-color: #000000;
    color: #f8f9fa; 
    font-family: 'Inter', sans-serif; 
}
.block-container { padding-top: 5rem !important; max-width: 850px !important; }

/* 1. Brand Identity */
.brand-box { margin-bottom: 60px; text-align: left; animation: fadeIn 1.2s ease-out; }
.brand-logo {
    font-weight: 800; font-size: 2.5rem; letter-spacing: -1.5px;
    background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    display: inline-block;
}
.brand-meta { font-size: 10px; font-weight: 600; color: #5f6368; letter-spacing: 5px; text-transform: uppercase; margin-top: 10px; }

/* 2. Neural Terminal */
.stTextArea textarea { 
    background-color: rgba(255, 255, 255, 0.015) !important; 
    border: 1px solid rgba(255, 255, 255, 0.08) !important; 
    border-radius: 28px !important; 
    color: #ffffff !important; 
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 15px !important; padding: 30px !important; line-height: 1.8;
    min-height: 380px !important; transition: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.stTextArea textarea:focus { border-color: #4285F4 !important; background-color: rgba(66, 133, 244, 0.04) !important; }

/* 3. Catalyst Button */
div.stButton > button {
    background: linear-gradient(90deg, #4285F4, #9B72CB) !important;
    color: #ffffff !important; font-weight: 700 !important; font-size: 1.05rem !important;
    border-radius: 100px !important; padding: 16px 60px !important;
    width: auto !important; border: none !important; margin: 20px 0;
    transition: 0.3s all cubic-bezier(0.16, 1, 0.3, 1);
}
div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 10px 40px rgba(155, 114, 203, 0.4); }

/* 4. Authority Reveal */
.result-card {
    background: rgba(255, 255, 255, 0.01);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 70px 50px; border-radius: 40px; margin-top: 60px;
    box-shadow: 0 40px 100px rgba(0,0,0,0.8);
}
.score-hero { font-size: 9rem; font-weight: 800; color: #ffffff; line-height: 0.85; margin: 25px 0; letter-spacing: -8px; }

/* 5. Viral Share Button (Premium Hook) */
.x-share-container { margin: 30px 0 50px 0; text-align: left; }
.x-share-btn { 
    display: inline-flex; align-items: center; gap: 12px;
    background: #ffffff; color: #000000 !important; 
    padding: 14px 32px; border-radius: 100px; 
    text-decoration: none; font-weight: 700; font-size: 0.95rem;
    transition: 0.4s all cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.x-share-btn:hover { background: #00f0ff; transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0, 240, 255, 0.3); }
.x-share-btn svg { width: 18px; height: 18px; fill: currentColor; }

/* 6. Strategic Strengths (The Ego Builder) */
.strength-card {
    background: rgba(138, 180, 248, 0.03);
    border: 1px solid rgba(138, 180, 248, 0.1);
    padding: 30px; border-radius: 20px; margin-bottom: 30px;
}
.s-tag { color: #8ab4f8; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; display: block; }
.s-text { font-size: 1.1rem; color: #ffffff; font-weight: 500; line-height: 1.6; }

/* 7. Precision Risks */
.finding-box { border-top: 1px solid rgba(255, 255, 255, 0.05); padding: 50px 0; margin-top: 50px; }
.f-tag { color: #ff6b6b; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 20px; display: block; }
.f-title { font-size: 2.2rem; font-weight: 700; color: #ffffff; margin-bottom: 20px; line-height: 1.1; letter-spacing: -1.5px; }
.f-impact { font-size: 1.2rem; color: #9aa0a6; line-height: 1.8; }

/* 8. The Master Blueprint (The Real Value) */
.blueprint-card {
    background: linear-gradient(180deg, rgba(227, 179, 65, 0.08) 0%, rgba(0,0,0,0) 100%);
    border: 1px solid rgba(227, 179, 65, 0.3);
    padding: 60px; border-radius: 32px; margin-top: 40px;
}
.blueprint-label { font-size: 12px; font-weight: 800; color: #e3b341; letter-spacing: 6px; text-transform: uppercase; margin-bottom: 35px; display: block; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
</style>
''', unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR
# ────────────────────────────────────────────────
def send_radar(score, issues_count, latency=0):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = (f"🛡️ *AEGIS AUTHORITY REPORT*\n\n● *INTEGRITY:* {score}%\n● *RISKS:* {issues_count}\n"
                   f"● *LATENCY:* {latency:.2f}s\n\n📡 _WAT SYSTEMS AUTHORITY_")
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (FULL SPECTRUM PROMPT)
# ────────────────────────────────────────────────
def run_audit(payload):
    start_t = time.time()
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "Secrets Missing.", "the_cure": "Configure API Key."}]}

    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    
    last_err = ""
    for model in model_pool:
        try:
            # 💎 FULL SPECTRUM VALUE PROMPT (Re-added Strengths)
            prompt = (
                "You are AEGIS, the Lead Solutions Architect. Analyze for fatal logic failures. "
                "Output JSON ONLY. "
                "1. STRENGTHS: Highlight 2-3 valid architectural or logic wins (The Ego Builder). "
                "2. FINDINGS: Provide critical failures. "
                "3. THE CURE: An EXHAUSTIVE 100x Value Master-Grade Blueprint: "
                "A) ROOT CAUSE: Deep architectural why. B) REMEDIATION: Senior-level clean code. C) REFACTOR: Prevention strategy."
                "Format: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
            )
            
            payload_data = {
                "model": model,
                "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": f"AUDIT:\n{payload[:15000]}"}],
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
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if match: 
                    result = json.loads(match.group(0), strict=False)
                    latency = time.time() - start_t
                    send_radar(result.get('trust_score', 0), len(result.get('findings', [])), latency)
                    return result
            last_err = f"API {resp.status_code}: {resp.text}"
        except Exception as e:
            last_err = str(e)
            continue
            
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Check credits."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown('<div class="brand-box"><h1 class="brand-logo">AEGIS Neural</h1><div class="brand-meta">NEURAL LOGIC AUTHORITY — WAT SYSTEMS</div></div>', unsafe_allow_html=True)

payload = st.text_area("", placeholder="How can AEGIS dissect your logic today? Paste DNA for audit...")

if st.button("Dissect Neural Pathways"):
    if not payload.strip(): st.error("NULL_PAYLOAD")
    else:
        with st.spinner("Analyzing structural DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (FULL SPECTRUM EXPERIENCE)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#58a6ff; font-weight:800; font-size:12px; letter-spacing:2px;'>NEURAL INTEGRITY</div><div class='score-hero'>{score}%</div>", unsafe_allow_html=True)
    
    # Viral Share Section
    share_msg = f"My logic scored {score}% on AEGIS Neural Auditor. Verified by WAT SYSTEMS 🛡️✦"
    share_url = f"https://x.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f'''
        <div class="x-share-container">
            <a href="{share_url}" target="_blank" class="x-share-btn">
                <svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>
                BROADCAST AUTHORITY
            </a>
        </div>
    ''', unsafe_allow_html=True)

    # Strategic Strengths (THE EGO BUILDER - RE-ADDED)
    st.write("")
    st.subheader("🛡️ STRATEGIC STRENGTHS")
    for s in res.get('strengths', []):
        st.markdown(f'<div class="strength-card"><span class="s-tag">VALIDATED WIN</span><div class="s-text">{s}</div></div>', unsafe_allow_html=True)

    # Detailed Risks
    st.write("")
    st.subheader("🚨 IDENTIFIED LOGIC FAILURES")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f'''
            <div class="finding-box">
                <span class="f-tag">ID_VULNERABILITY_{i+1:02}</span>
                <div class="f-title">{f.get('issue')}</div>
                <div class="f-impact"><b>CATASTROPHIC IMPACT:</b> {f.get('catastrophic_impact')}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        if not st.session_state.unlocked:
            st.markdown('<div class="blueprint-card" style="text-align:center;"><span class="blueprint-label">🔒 SOVEREIGN BLUEPRINT ENCRYPTED</span><div style="color:#555; font-size:14px;">Secure Enterprise Pass to access 100X Value Mastery Blueprint.</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="blueprint-card"><span class="blueprint-label">💎 MASTER-GRADE TECHNICAL BLUEPRINT</span></div>', unsafe_allow_html=True)
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
    if st.button("New Scan Session", type="secondary"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown('<div style="text-align:center; color:#222; font-size:11px; margin-top:10rem; padding-bottom:5rem; letter-spacing:10px; font-weight:800;">WAT SYSTEMS | AEGIS v48.0 | SOVEREIGN AUTHORITY</div>', unsafe_allow_html=True)
