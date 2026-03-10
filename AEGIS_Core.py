import streamlit as st
import json
import requests
import urllib.parse

# ────────────────────────────────────────────────
# 1. ENTERPRISE DESIGN SYSTEM (ULTRA-PREMIUM)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | WAT SYSTEMS", 
    layout="centered", 
    page_icon="🛡️"
)

# Initialize States (System Logic Unchanged)
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# The Obsidian Design Framework
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@500&display=swap');

    /* Global Reset */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { 
        background-color: #000000; 
        color: #ededed; 
        font-family: 'Inter', sans-serif; 
    }

    /* Sovereign Brand Header */
    .enterprise-header {
        padding: 100px 0 60px 0;
        text-align: center;
    }
    .brand-logo {
        font-weight: 800;
        font-size: 4.5rem;
        letter-spacing: -4px;
        color: #ffffff;
        margin: 0;
        line-height: 0.8;
    }
    .brand-tagline {
        font-size: 11px;
        font-weight: 600;
        color: #666666;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-top: 20px;
    }

    /* High-Fidelity Module Grid */
    .module-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1px;
        background: #1a1a1a;
        border: 1px solid #1a1a1a;
        margin-bottom: 50px;
    }
    .module-item {
        background: #000000;
        padding: 25px;
        text-align: center;
    }
    .m-status { font-size: 8px; font-weight: 800; color: #0070f3; text-transform: uppercase; display: block; margin-bottom: 8px; }
    .m-name { font-size: 12px; font-weight: 600; color: #ffffff; }

    /* The Intelligence Terminal */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 0px !important; 
        color: #ededed !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 40px !important;
        line-height: 1.8;
        transition: 0.3s;
    }
    .stTextArea textarea:focus { border-color: #333333 !important; background-color: #080808 !important; }

    /* Action Trigger (Billion-Dollar CTA) */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border-radius: 4px !important;
        padding: 24px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1);
        margin-top: 30px;
    }
    div.stButton > button:hover { 
        background-color: #0070f3 !important; 
        color: #ffffff !important;
        transform: translateY(-2px);
    }

    /* Result Authority Section */
    .result-dashboard {
        border: 1px solid #1a1a1a;
        padding: 80px 60px;
        margin-top: 100px;
        background: #000000;
    }
    .score-title { font-size: 12px; font-weight: 600; color: #666666; letter-spacing: 4px; text-transform: uppercase; }
    .score-display { font-size: 140px; font-weight: 800; color: #ffffff; letter-spacing: -12px; line-height: 1; margin: 20px 0; }
    .score-badge { display: inline-block; background: #0070f3; color: white; padding: 4px 12px; font-size: 10px; font-weight: 800; letter-spacing: 2px; }

    /* Freemium Findings (High Detail) */
    .finding-block {
        border-top: 1px solid #1a1a1a;
        padding: 40px 0;
        margin-top: 40px;
    }
    .finding-id { font-size: 10px; font-weight: 800; color: #ff4d4d; text-transform: uppercase; margin-bottom: 15px; display: block; }
    .finding-title { font-size: 22px; font-weight: 600; color: #ffffff; margin-bottom: 10px; }
    .finding-impact { font-size: 16px; color: #888888; line-height: 1.6; }

    /* The Cure: Exclusive Path */
    .cure-locked {
        background: #050505;
        border: 1px solid #332b00;
        padding: 40px;
        text-align: center;
        margin-top: 25px;
    }
    .locked-label { font-size: 10px; font-weight: 800; color: #eae100; letter-spacing: 3px; text-transform: uppercase; }

    /* Viral Integration */
    .x-share-container { text-align: center; margin-top: 60px; padding-top: 60px; border-top: 1px solid #1a1a1a; }
    .x-share-btn { 
        display: inline-block; 
        border: 1px solid #333333; 
        color: #ffffff !important; 
        padding: 15px 40px; 
        border-radius: 4px; 
        text-decoration: none; 
        font-weight: 600; 
        font-size: 13px; 
        transition: 0.3s;
    }
    .x-share-btn:hover { background: #ffffff; color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (SYSTEM LOGIC)
# ────────────────────────────────────────────────
def send_radar(score, issues_count, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *[AEGIS AUTHORITY]*\n\n● *Status:* {status}\n● *Score:* {score}%\n● *Findings:* {issues_count}\n\n📡 _WAT SYSTEMS_"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=5)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME ENGINE (SYSTEM LOGIC)
# ────────────────────────────────────────────────
def run_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key: return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "API Key Missing.", "the_cure": "Set Secrets."}]}

    model_pool = ["google/gemini-2.0-flash-001", "google/gemini-flash-1.5", "meta-llama/llama-3.3-70b-instruct"]
    last_err = ""
    for model in model_pool:
        try:
            resp = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": model,
                    "messages": [{"role": "system", "content": "You are AEGIS, the supreme Logic Auditor. Identify ALL structural and logic vulnerabilities. Be factual, professional, and brutal. Provide a detailed multi-point audit. Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"},
                                 {"role": "user", "content": payload[:12000]}],
                    "temperature": 0.0,
                    "response_format": {"type": "json_object"}
                }), timeout=40
            )
            if resp.status_code == 200:
                result = json.loads(resp.json()['choices'][0]['message']['content'])
                send_radar(result.get('trust_score', 0), len(result.get('findings', [])))
                return result
            last_err = resp.text
        except Exception as e: last_err = str(e)
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_err, "the_cure": "Verify API Status."}]}

# ────────────────────────────────────────────────
# 4. INTERFACE ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='enterprise-header'>
        <h1 class='brand-logo'>AEGIS</h1>
        <div class='brand-tagline'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

# Module Grid (Industrial Look)
st.markdown("""
    <div class='module-grid'>
        <div class='module-item'><span class='m-status'>Online</span><span class='m-name'>CODE SECURITY</span></div>
        <div class='module-item'><span class='m-status'>Online</span><span class='m-name'>WORKFLOW LOGIC</span></div>
        <div class='module-item'><span class='m-status'>Online</span><span class='m-name'>SMART CONTRACTS</span></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=350, placeholder="/// PASTE LOGIC DNA FOR AUDIT")

if st.button("EXECUTE SUPREME AUDIT"):
    if not payload.strip(): st.error("ERROR: NULL DATA.")
    else:
        with st.spinner("Decoding DNA..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (PREMIUM FREEMIUM)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-dashboard'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-title'>GLOBAL TRUST SCORE</div><div class='score-display'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div class='score-badge'>VALIDATED BY AEGIS CORE</div>", unsafe_allow_html=True)
    
    # Viral X-Share
    share_msg = f"My project logic scored {score}% on AEGIS. Verified by WAT SYSTEMS. 🛡️🔥 Check yours:"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div class='x-share-container'><a href='{share_url}' target='_blank' class='x-share-btn'>SHARE AUTHORITY ON 𝕏</a></div>", unsafe_allow_html=True)

    # Detailed Freemium Findings
    st.write("")
    st.subheader("🚨 CRITICAL LOGIC VULNERABILITIES")
    for i, f in enumerate(res.get("findings", [])):
        st.markdown(f"""
            <div class='finding-block'>
                <span class='finding-id'>RISK MODULE {i+1:02}</span>
                <div class='finding-title'>{f.get('issue')}</div>
                <div class='finding-impact'><b>ANALYSIS:</b> "{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall for The Cure
        if not st.session_state.unlocked:
            st.markdown("<div class='cure-locked'><span class='locked-label'>🔒 REMEDIATION ENCRYPTED</span></div>", unsafe_allow_html=True)
        else:
            st.success("**THE CURE (TECHNICAL SOLUTION):**")
            st.code(f.get('the_cure'), language='python')

    # Global Unlock Experience
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 SECURE ENTERPRISE PASS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        passcode = st.text_input("INPUT ACCESS PASSCODE:", type="password")
        if st.button("UNLOCK DEPLOYMENT"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS DENIED.")

    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#222; font-size:10px; margin-top:150px; font-weight:600; letter-spacing:6px;'>WAT SYSTEMS | AEGIS v31.0 | SUPREME AUTHORITY</div>", unsafe_allow_html=True)
