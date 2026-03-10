import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. SOVEREIGN INDUSTRIAL UI (FINAL PREMIUM STANDARD)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | UNIVERSAL AUTHORITY", 
    layout="centered", 
    page_icon="🛡️"
)

# Persistence Control
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# Premium Authority Styling - Absolute Obsidian
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { 
        background-color: #050505; 
        color: #e6edf3; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }

    /* Sovereign Brand Identity */
    .brand-header { padding: 80px 0 40px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 50px; }
    .logo-main { font-weight: 800; font-size: 3.2rem; letter-spacing: -3px; color: #ffffff; margin: 0; line-height: 1; }
    .logo-sub { font-size: 10px; font-weight: 700; color: #58a6ff; letter-spacing: 7px; text-transform: uppercase; margin-top: 10px; opacity: 0.8; }

    /* Matrix Pillars Matrix */
    .pillar-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 35px; }
    .pillar-box { 
        background: rgba(255,255,255,0.02); 
        border: 1px solid rgba(255,255,255,0.05); 
        padding: 20px; 
        border-radius: 4px; 
        text-align: left;
        border-left: 3px solid #30363d;
    }
    .p-tag { font-size: 8px; font-weight: 800; color: #8b949e; text-transform: uppercase; }
    .p-val { font-size: 11px; font-weight: 700; color: #ffffff; margin-top: 5px; }

    /* The Obsidian Terminal */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 4px !important; 
        color: #f0f6fc !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 30px !important;
        line-height: 1.7;
        box-shadow: inset 0 0 30px rgba(0,0,0,1) !important;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; }

    /* Executive Execution Button */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 4px !important;
        padding: 22px 0 !important;
        width: 100% !important;
        border: 1px solid #ffffff !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        transition: 0.2s all cubic-bezier(0.16, 1, 0.3, 1);
        margin-top: 25px;
    }
    div.stButton > button:hover { 
        background-color: #58a6ff !important; 
        border-color: #58a6ff !important;
        color: #ffffff !important; 
        transform: translateY(-2px);
        box-shadow: 0 10px 40px rgba(88, 166, 255, 0.25);
    }

    /* Result Section */
    .result-aura { 
        background: #000000; 
        border: 1px solid #1a1a1a; 
        padding: 80px 60px; 
        margin-top: 80px; 
        border-top: 8px solid #58a6ff;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }
    .score-label { font-size: 12px; font-weight: 700; color: #8b949e; letter-spacing: 5px; text-transform: uppercase; }
    .score-val { font-size: 120px; font-weight: 800; color: #ffffff; letter-spacing: -10px; line-height: 1; margin: 25px 0; }
    
    /* Detailed Finding Cards */
    .finding-card { 
        background: rgba(255,255,255,0.01); 
        border: 1px solid rgba(255,255,255,0.05); 
        padding: 35px; 
        border-radius: 4px; 
        margin-top: 25px; 
        border-left: 6px solid #f85149; 
    }
    .finding-title { font-weight: 800; color: #ffffff; font-size: 18px; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .finding-impact { font-size: 15px; color: #8b949e; line-height: 1.6; }

    /* The Cure Paywall */
    .cure-paywall { 
        background: #050505; 
        border: 1px solid #e3b341; 
        padding: 45px; 
        border-radius: 4px; 
        text-align: center; 
        margin-top: 30px;
    }
    .locked-tag { font-size: 10px; font-weight: 800; color: #e3b341; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 12px; display: block; }

    /* X-Share Loop Button */
    .x-btn { 
        display: inline-block; 
        background: #ffffff; 
        color: #000000 !important; 
        padding: 18px 45px; 
        border-radius: 50px; 
        text-decoration: none; 
        font-weight: 800; 
        font-size: 12px; 
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 35px;
        transition: 0.3s;
    }
    .x-btn:hover { background: #58a6ff; color: white !important; transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (PRIORITY 0)
# ────────────────────────────────────────────────
def send_telegram_radar(score, issues, status="SUCCESS"):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            icon = "🛡️" if status == "SUCCESS" else "🚨"
            issue_desc = issues[0].get('issue', 'N/A') if issues else 'N/A'
            msg = (
                f"{icon} *[AEGIS RADAR ALERT]*\n\n"
                f"● *STATUS:* {status}\n"
                f"● *LOGIC SCORE:* {score}%\n"
                f"● *PRIMARY RISK:* {issue_desc}\n\n"
                f"📡 _Authority: WAT SYSTEMS_"
            )
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=12)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME AUDIT ENGINE (ULTRA RESILIENCE)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    send_telegram_radar(0, [], status="AUDIT_INITIATED")
    
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"trust_score": 0, "findings": [{"issue": "UPLINK_FAILURE", "catastrophic_impact": "Secrets Missing.", "the_cure": "Configure Secrets."}]}

    # Updated Model Pool (Confirmed Active as of now)
    # We remove problematic exp models and use stable free-tier ones.
    model_pool = [
        "google/gemini-2.0-flash-001:free",
        "deepseek/deepseek-r1:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemini-flash-1.5-8b:free"
    ]
    
    last_error = ""
    for model in model_pool:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://aegis.watsystems.tech",
                    "X-Title": "AEGIS v28 Authority",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system", 
                            "content": (
                                "You are AEGIS, the supreme Logic Auditor by WAT SYSTEMS. "
                                "Identify ALL structural and logic vulnerabilities. Be factual, professional, and brutal. "
                                "Provide a detailed multi-point audit. Justify the score. "
                                "Output JSON ONLY: {\"trust_score\": int, \"strengths\": [\"str\"], \"findings\": [{\"issue\": \"str\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}]}"
                            )
                        },
                        {"role": "user", "content": f"AUDIT_TARGET:\n{payload[:15000]}"}
                    ],
                    "temperature": 0.0,
                    "response_format": {"type": "json_object"}
                }),
                timeout=50
            )
            
            if response.status_code == 200:
                result = response.json()
                raw_content = result['choices'][0]['message']['content'].strip()
                data = json.loads(raw_content)
                send_telegram_radar(data.get('trust_score', 0), data.get('findings', []))
                return data
            else:
                # Log detailed error from OpenRouter for fallback debugging
                try:
                    error_json = response.json()
                    msg = error_json.get('error', {}).get('message', str(error_json))
                    last_error = f"API {response.status_code} ({model}): {msg}"
                except:
                    last_error = f"API Error {response.status_code} for {model}"
                continue 
                
        except Exception as e:
            last_error = f"Model {model} failed: {str(e)}"
            continue

    send_telegram_radar(0, [], status="SYSTEM_CRASH")
    return {"trust_score": 0, "findings": [{"issue": "TOTAL_UPLINK_FAILURE", "catastrophic_impact": last_error, "the_cure": "Check API Keys or verify OpenRouter Credits."}]}

# ────────────────────────────────────────────────
# 4. SYSTEM INTERFACE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='brand-header'>
        <div class='logo-main'>AEGIS</div>
        <div class='logo-sub'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='pillar-row'>
        <div class='pillar-box'><span class='p-tag'>AUDIT-01</span><div class='p-name'>CODE AUDIT</div></div>
        <div class='pillar-box'><span class='p-tag'>AUDIT-02</span><div class='p-name'>LOGIC FLOW</div></div>
        <div class='pillar-box'><span class='p-tag'>AUDIT-03</span><div class='p-name'>WEB3 SECURITY</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD FOR DISSECTION:", height=320, placeholder="/// PASTE ARCHITECTURAL DATA")

if st.button("EXECUTE SUPREME AUDIT (DETAILED SCAN)"):
    if not payload.strip():
        st.error("SYSTEM ERROR: NULL DATA.")
    else:
        with st.spinner("Decoding DNA..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. THE REVEAL (PREMIUM FREEMIUM)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='color: #58a6ff; font-weight: 800; font-size: 11px; letter-spacing: 4px; margin-bottom: 30px;'>VALIDATED BY AEGIS CORE AUTHORITY</div>", unsafe_allow_html=True)
    
    # Viral Loop: โชว์คะแนน
    share_msg = f"My project logic scored {score}% on AEGIS. God-tier validation by WAT SYSTEMS. 🛡️🔥"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<div style='text-align:center;'><a href='{share_url}' target='_blank' class='x-btn'>𝕏 BROADCAST AUTHORITY</a></div>", unsafe_allow_html=True)

    # Detailed Risks
    st.write("")
    st.subheader("🚨 DETECTED LOGIC FAILURES")
    findings = res.get("findings", [])
    
    for i, f in enumerate(findings):
        st.markdown(f"""
            <div class='finding-card'>
                <div class='finding-title'>RISK-{i+1:02}: {f.get('issue')}</div>
                <div class='finding-impact'><b>IMPACT ANALYSIS:</b> "{f.get('catastrophic_impact')}"</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall for The Cure
        if not st.session_state.unlocked:
            st.markdown(f"""
                <div class='cure-paywall'>
                    <span class='locked-tag'>🔒 REMEDIATION ENCRYPTED</span>
                    <div style='color:#8b949e; font-size:12px;'>Enterprise Pass required to decrypt technical solution for this vulnerability.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success("**THE CURE (TECHNICAL SOLUTION):**")
            st.code(f.get('the_cure'), language='python')

    # Premium Conversion
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 UNLOCK ALL TECHNICAL REMEDIATIONS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        
        st.write("")
        passcode = st.text_input("ENTER ACCESS PASSCODE:", type="password")
        if st.button("🔓 DEPLOY SOLUTIONS"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("ACCESS DENIED.")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#1a1a1a; font-size:10px; margin-top:140px; font-weight:700; letter-spacing:6px;'>WAT SYSTEMS | AEGIS v28.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
