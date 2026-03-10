import streamlit as st
import json
import requests
import urllib.parse
import time

# ────────────────────────────────────────────────
# 1. SOVEREIGN INDUSTRIAL UI (PREMIUM EXPERIENCE)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS | GLOBAL AUTHORITY", 
    layout="centered", 
    page_icon="🛡️"
)

# Persistence Control
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    
    .main { 
        background-color: #000000; 
        color: #ffffff; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }

    /* Brand Identity */
    .brand-header { padding: 50px 0; border-bottom: 1px solid #1a1a1a; margin-bottom: 40px; }
    .logo-main { font-weight: 800; font-size: 2.8rem; letter-spacing: -2px; color: #ffffff; margin: 0; }
    .logo-sub { font-size: 10px; font-weight: 700; color: #58a6ff; letter-spacing: 5px; text-transform: uppercase; margin-top: 5px; }

    /* Matrix Pillar Display */
    .pillar-row { display: flex; gap: 15px; margin-bottom: 30px; }
    .pillar-box { flex: 1; background: #080808; border: 1px solid #1a1a1a; padding: 15px; border-radius: 4px; text-align: left; border-left: 2px solid #30363d; }
    .p-tag { font-size: 8px; font-weight: 800; color: #8b949e; text-transform: uppercase; }
    .p-val { font-size: 11px; font-weight: 700; color: #f0f6fc; margin-top: 4px; }

    /* The Obsidian Terminal */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        border: 1px solid #1a1a1a !important; 
        border-radius: 4px !important; 
        color: #f0f6fc !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 15px !important;
        padding: 30px !important;
        line-height: 1.6;
    }
    .stTextArea textarea:focus { border-color: #58a6ff !important; }

    /* Action Buttons */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 2px !important;
        padding: 20px 0 !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 4px !important;
        transition: 0.2s all;
    }
    div.stButton > button:hover { background-color: #58a6ff !important; color: #ffffff !important; }

    /* Detailed Result Section */
    .result-aura { background: #000000; border: 1px solid #1a1a1a; padding: 60px; margin-top: 60px; border-top: 5px solid #58a6ff; }
    .score-label { font-size: 11px; font-weight: 700; color: #8b949e; letter-spacing: 4px; }
    .score-val { font-size: 110px; font-weight: 800; color: #ffffff; letter-spacing: -6px; line-height: 1; margin: 20px 0; }
    
    /* Detailed Finding Cards (Freemium Value) */
    .finding-card { background: rgba(255,255,255,0.02); border: 1px solid #1a1a1a; padding: 25px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #f85149; }
    .finding-title { font-weight: 800; color: #ffffff; font-size: 16px; margin-bottom: 10px; }
    .finding-impact { font-size: 14px; color: #8b949e; line-height: 1.5; }

    /* Paywall: The Cure */
    .cure-paywall { background: #080808; border: 1px solid #e3b341; padding: 30px; border-radius: 8px; text-align: center; margin-top: 20px; }
    .locked-text { font-size: 10px; font-weight: 800; color: #e3b341; letter-spacing: 2px; text-transform: uppercase; }

    /* Viral Share Button */
    .share-btn { display: inline-block; background: #1da1f2; color: white !important; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 13px; margin-top: 20px; transition: 0.3s all; }
    .share-btn:hover { background: #1a91da; transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. TELEGRAM RADAR (PRIORITY 0)
# ────────────────────────────────────────────────
def send_telegram_radar(score, issues_count):
    try:
        token = st.secrets.get("TELEGRAM_BOT_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            msg = f"🛡️ *[AEGIS AUTHORITY]*\n\n● *Status:* Audit Complete\n● *Score:* {score}%\n● *Risks Found:* {issues_count}\n\n📡 _Operational: WAT SYSTEMS_"
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                          data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=8)
    except: pass

# ────────────────────────────────────────────────
# 3. SUPREME AUDIT ENGINE (HIGH-DETAIL SCAN)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    api_key = st.secrets.get("OPENROUTER_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"trust_score": 0, "findings": [{"issue": "SYSTEM_BLIND", "catastrophic_impact": "API Key missing.", "the_cure": "Configure Secrets."}]}

    try:
        # ใช้ Gemini 2.0 Flash สำหรับความเร็วและความฉลาดในระดับ Freemium
        target_model = "google/gemini-2.0-flash-001:free"
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            data=json.dumps({
                "model": target_model,
                "messages": [
                    {
                        "role": "system", 
                        "content": (
                            "You are AEGIS, the supreme Logic Auditor by WAT SYSTEMS. "
                            "Provide a high-detail audit. Be brutal, factual, and expert. "
                            "Analyze strengths and find ALL critical logic flaws. "
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
        
        if response.status_code != 200: raise Exception(f"API Error: {response.status_code}")
            
        result = response.json()
        raw_content = result['choices'][0]['message']['content'].strip()
        data = json.loads(raw_content)
        
        # ส่งเรดาร์แจ้งเตือนสถาปนิก
        send_telegram_radar(data.get('trust_score', 0), len(data.get('findings', [])))
        
        return data
        
    except Exception as e:
        return {"trust_score": 0, "findings": [{"issue": "UPLINK FAILURE", "catastrophic_impact": str(e), "the_cure": "Check API Credentials."}]}

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
        <div class='pillar-box'><span class='p-tag'>MOD-01</span><div class='p-name'>CODE AUDIT</div></div>
        <div class='pillar-box'><span class='p-tag'>MOD-02</span><div class='p-name'>LOGIC FLOW</div></div>
        <div class='pillar-box'><span class='p-tag'>MOD-03</span><div class='p-name'>WEB3 SECURITY</div></div>
    </div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=300, placeholder="Paste your architectural logic or source code here for a professional audit...")

if st.button("RUN GLOBAL AUDIT (DETAILED SCAN)"):
    if not payload.strip():
        st.error("SYSTEM ERROR: Null data.")
    else:
        with st.spinner("Decoding structural integrity..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 5. AUDIT REVEAL (THE AUTHORITY DISPLAY)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("<div class='result-aura'>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-label'>GLOBAL LOGIC SCORE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-val'>{score}%</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:#58a6ff; color:#000; padding:2px 10px; font-size:10px; font-weight:800;'>AUDIT COMPLETE | VALIDATED BY AEGIS</div>", unsafe_allow_html=True)
    
    # Viral Share on X
    share_msg = f"My project logic scored {score}% on AEGIS Auditor. God-tier validation by WAT SYSTEMS. 🛡️🔥 Check your authority here:"
    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_msg)}&url=https://aegis-auditor.streamlit.app"
    st.markdown(f"<a href='{share_url}' target='_blank' class='share-btn'>𝕏 SHARE YOUR SCORE</a>", unsafe_allow_html=True)

    # Detailed Findings (Freemium Value)
    st.write("")
    st.subheader("🛡️ STRUCTURAL STRENGTHS")
    for s in res.get('strengths', []):
        st.success(f"**VALIDATED:** {s}")

    st.write("")
    st.subheader("🚨 DETECTED RISKS & VULNERABILITIES")
    findings = res.get("findings", [])
    
    for i, f in enumerate(findings):
        st.markdown(f"""
            <div class='finding-card'>
                <div class='finding-title'>RISK-{i+1:02}: {f.get('issue')}</div>
                <div class='finding-impact'><b>IMPACT:</b> {f.get('catastrophic_impact')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Paywall per finding
        if not st.session_state.unlocked:
            st.markdown(f"""
                <div class='cure-paywall'>
                    <div class='locked-text'>🔒 SOLUTION ENCRYPTED</div>
                    <div style='color:#8b949e; font-size:11px; margin-top:5px;'>Enterprise pass required to unlock the remediation code for this risk.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"**THE CURE (REMEDIATION):**")
            st.code(f.get('the_cure'))

    # Global Unlock
    if not st.session_state.unlocked:
        st.write("")
        st.link_button("👉 UNLOCK ALL TECHNICAL SOLUTIONS ($9)", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
        passcode = st.text_input("INPUT PASSCODE:", type="password")
        if st.button("UNLOCK DEPLOYMENT"):
            if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                st.session_state.unlocked = True
                st.rerun()
            else: st.error("Access Denied.")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("RESET AUDIT TERMINAL"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#222; font-size:9px; margin-top:100px; font-weight:700; letter-spacing:5px;'>WAT SYSTEMS | AEGIS v23.0 | SOVEREIGN AUTHORITY</div>", unsafe_allow_html=True)
