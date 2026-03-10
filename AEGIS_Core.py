import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. INDUSTRIAL AUTHORITY UI SYSTEM
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | WAT SYSTEMS", 
    layout="centered", 
    page_icon="🛡️"
)

if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# Obsidian Absolute Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Space+Mono&display=swap');
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }

    /* Brand Architecture */
    .brand-header { padding: 60px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 50px; }
    .logo-main { font-weight: 900; font-size: 3.5rem; letter-spacing: -3px; color: #ffffff; margin: 0; line-height: 1; }
    .logo-sub { font-size: 10px; font-weight: 700; color: #58a6ff; letter-spacing: 6px; text-transform: uppercase; margin-top: 10px; opacity: 0.8; }

    /* Industrial Matrix Pillars */
    .pillar-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 40px; }
    .pillar-box { background: #050505; border: 1px solid #1a1a1a; padding: 20px; border-radius: 0px; border-left: 3px solid #30363d; }
    .p-tag { font-size: 8px; font-weight: 800; color: #8b949e; text-transform: uppercase; }
    .p-val { font-size: 11px; font-weight: 700; color: #f0f6fc; margin-top: 5px; }

    /* Terminal Interface */
    .stTextArea textarea { 
        background-color: #000000 !important; border: 1px solid #1a1a1a !important; border-radius: 0px !important; 
        color: #f0f6fc !important; font-family: 'Space Mono', monospace !important; font-size: 14px !important; 
        padding: 30px !important; line-height: 1.7; box-shadow: none !important;
    }

    /* Executive Action Button */
    div.stButton > button {
        background-color: #ffffff !important; color: #000000 !important; font-weight: 800 !important; 
        border-radius: 0px !important; padding: 25px 0 !important; width: 100% !important; border: none !important; 
        text-transform: uppercase !important; letter-spacing: 5px !important; transition: 0.2s all;
    }
    div.stButton > button:hover { background-color: #58a6ff !important; color: #ffffff !important; }

    /* Result Displays */
    .result-aura { background: #000000; border: 1px solid #1a1a1a; padding: 80px 60px; margin-top: 80px; border-top: 8px solid #58a6ff; }
    .score-label { font-size: 12px; font-weight: 700; color: #8b949e; letter-spacing: 5px; text-transform: uppercase; }
    .score-val { font-size: 130px; font-weight: 800; color: #ffffff; letter-spacing: -10px; line-height: 1; margin: 30px 0; }
    
    .finding-card { background: #050505; border: 1px solid #1a1a1a; padding: 35px; margin-top: 25px; border-left: 6px solid #f85149; }
    .finding-title { font-weight: 800; color: #ffffff; font-size: 20px; text-transform: uppercase; margin-bottom: 10px; }
    .finding-impact { font-size: 15px; color: #8b949e; line-height: 1.7; font-style: italic; }

    .cure-paywall { background: #000000; border: 1px solid #e3b341; padding: 40px; text-align: center; margin-top: 20px; }
    .x-btn { display: inline-block; background: #ffffff; color: #000000 !important; padding: 15px 40px; border-radius: 0px; text-decoration: none; font-weight: 800; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="COMPLETE"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *[AEGIS AUTHORITY ALERT]*\n\n● *Status:* {status}\n● *Score:* {score}%\n● *Findings:* {issues_count}\n\n📡 _WAT SYSTEMS_"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (RESILIENT AUTO-ROUTING)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    # ใช้โมเดลแบบกว้างและเสถียรที่สุดเพื่อเลี่ยง 404/400
    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    
    last_err = ""
    for model in model_pool:
        try:
            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "system", "content": "You are AEGIS, a brutal Logic Auditor. Find ALL flaws. Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                                 {"role": "user", "content": payload[:12000]}],
                    "temperature": 0.0,
                    "response_format": {"type": "json_object"}
                }), timeout=40
            )
            if resp.status_code == 200:
                data = resp.json()['choices'][0]['message']['content']
                result = json.loads(data)
                send_radar(result.get('trust_score', 0), len(result.get('findings', [])))
                return result
            last_err = resp.text
        except Exception as e: last_err = str(e)
    
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Verify API Credits."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("<div class='brand-header'><div class='logo-main'>AEGIS</div><div class='logo-sub'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-box'><span class='p-tag'>MOD-01</span><div class='p-val'>CODE SECURITY</div></div>
        <div class='pillar-box'><span class='p-tag'>MOD-02</span><div class='p-val'>WORKFLOW LOGIC</div></div>
        <div class='pillar-box'><span class='p-tag'>MOD-03</span><div class='p-val'>SMART CONTRACTS</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=300, placeholder="/// PASTE ARCHITECTURAL DATA")

if st.button("EXECUTE GLOBAL AUDIT"):
    if not payload.strip(): st.error("ERROR: NULL DATA.")
    else:
        with st.spinner("Decoding DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div><div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    
    share_msg = f"My project logic scored {score}% on AEGIS. Verified by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div style='text-align:center;'><a href='{share_url}' target='_blank' class='x-btn'>𝕏 SHARE AUTHORITY</a></div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("🚨 DETECTED VULNERABILITIES")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"<div class='finding-card'><div class='finding-title'>RISK-{i+1:02}: {f.get('issue')}</div><div class='finding-impact'>\"{f.get('catastrophic_impact')}\"</div></div>", unsafe_allow_html=True)
        if not st.session_state.unlocked:
            st.markdown("<div class='cure-paywall'><div style='color:#e3b341; font-size:10px; font-weight:800;'>🔒 SOLUTION ENCRYPTED</div></div>", unsafe_allow_html=True)
        else:
            st.success("**THE CURE:**")
            st.code(f.get('the_cure'))

    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 UNLOCK ALL SOLUTIONS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        passcode = st.text_input("ACCESS PASSCODE:", type="password")
        if st.button("UNLOCK DEPLOYMENT"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("DENIED.")

    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#222; font-size:9px; margin-top:100px; font-weight:700; letter-spacing:6px;'>WAT SYSTEMS | AEGIS v30.0</div>", unsafe_allow_html=True)
