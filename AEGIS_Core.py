import streamlit as st
import json
import requests
import anthropic
import urllib.parse

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI CONFIG & NEURAL STYLING
# ────────────────────────────────────────────────
st.set_page_config(page_title="WAT SYSTEMS | AEGIS Global Authority", layout="centered", page_icon="🛡️")

# Initialize Session States
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

st.markdown("""
    <style>
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    .hero-container { text-align: center; padding: 50px 0 20px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 12px; font-weight: 900; margin-bottom: 5px; text-shadow: 0 0 50px rgba(88, 166, 255, 0.4); font-size: 3.5rem; }
    .brand-tag { color: #58a6ff; font-size: 11px; letter-spacing: 5px; font-weight: 800; margin-bottom: 50px; text-transform: uppercase; opacity: 0.8; }
    .score-display { background: #0d1117; padding: 45px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 30px 0; border-top: 6px solid #58a6ff; }
    .good-card { background: rgba(46, 160, 67, 0.08); border-left: 4px solid #2ea043; padding: 22px; border-radius: 10px; margin-bottom: 18px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .flaw-card { background: rgba(248, 81, 73, 0.08); border-left: 4px solid #f85149; padding: 28px; border-radius: 10px; margin-bottom: 30px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .locked-cure-box { background: repeating-linear-gradient( 45deg, rgba(227, 179, 65, 0.04), rgba(227, 179, 65, 0.04) 10px, rgba(0,0,0,0) 10px, rgba(0,0,0,0) 20px ); border: 2px dashed #e3b341; padding: 45px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    .unlocked-cure { background: rgba(46, 160, 67, 0.12); border: 1px solid #2ea043; padding: 35px; border-radius: 16px; color: #e6edf3; }
    div[data-testid="stExpander"] { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d !important; border-radius: 12px !important; }
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; font-family: 'Fira Code', monospace; font-size: 15px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. SUPREME AUDIT ENGINE (CLAUDE 3.5 SONNET)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Missing API Connection", "severity": "Critical", "catastrophic_impact": "System offline. Logic Authority requires a valid API link.", "the_cure": "Administrator: Insert ANTHROPIC_API_KEY in Secrets."}]}
        
        client = anthropic.Anthropic(api_key=api_key)
        system_prompt = (
            "You are AEGIS, a brutal, elite Universal Logic Auditor by WAT SYSTEMS. "
            "Analyze the payload strictly for logic flaws. Output JSON ONLY format: "
            "{"
            "  \"trust_score\": int, \"strengths\": [\"str\"], "
            "  \"findings\": [{\"issue\": \"str\", \"severity\": \"Critical\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}] "
            "}"
            "Be cold, direct, and authoritative. Respond ONLY with valid JSON."
        )
        
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=2500,
            temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": f"PAYLOAD:\n{payload[:12000]}"}]
        )
        
        raw_content = message.content[0].text.strip()
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_content)
    except Exception as e:
        return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Uplink Error", "severity": "Critical", "catastrophic_impact": str(e), "the_cure": "Check API Credits or Key Configuration."}]}

# ────────────────────────────────────────────────
# 3. UI ARCHITECTURE (3-PILLAR MATRIX)
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>AEGIS</h1><div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align:center; color:#238636; font-size:10px; font-weight:800; letter-spacing:3px; margin-bottom:40px;'>
        ● SYSTEM STATUS: ONLINE | LOGIC ENGINE: CLAUDE 3.5 SONNET
    </div>
""", unsafe_allow_html=True)

# Specialist Matrix - Focused on 3 Core Pillars
col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("💻 CODE SECURITY"): st.caption("Audit structural vulnerabilities.")
with col2:
    with st.expander("🤖 WORKFLOW LOGIC"): st.caption("Identify logic loops and bottlenecks.")
with col3:
    with st.expander("🔗 SMART CONTRACTS"): st.caption("Shield against Web3 exploits.")

st.write("")
payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste your architectural logic, code snippets, or business plans for a brutal audit...")

if st.button("🚀 INITIATE GLOBAL SCAN (FREE)"):
    if not payload.strip():
        st.error("❌ ERROR: No payload detected in the terminal.")
    else:
        with st.spinner("Decoding structural truth..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            # Silent Telegram Radar
            try:
                score = st.session_state.result.get('trust_score', 0)
                bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
                chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
                if bot_token and chat_id:
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text": f"🚨 [AEGIS RADAR] Audit Done. Score: {score}%"})
            except: pass
            st.rerun()

# ────────────────────────────────────────────────
# 4. RESULTS & NATIVE BUTTONS
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    st.markdown("---")
    
    st.markdown(f"""
        <div class='score-display'>
            <h3>GLOBAL TRUST SCORE</h3>
            <h1 style='font-size: 90px; color:#58a6ff; margin:0;'>{score}%</h1>
            <p style='color:#8b949e; letter-spacing:2px;'>Universal Logic Standard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Viral Loop - Share to X (Native Link)
    site_url = "https://aegis-auditor-rdztzsskvkrgaefesuzynl.streamlit.app/"
    tweet_text = f"My project logic scored {score}% on AEGIS. God-tier architecture validated by WAT SYSTEMS. 🛡️🔥 Test yours: {site_url}"
    x_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
    st.link_button("𝕏 SHARE YOUR SCORE ON X", x_url, use_container_width=True)
    st.write("")

    # ✅ Strengths
    strengths = res.get("strengths", [])
    if strengths:
        st.subheader("✅ ARCHITECTURAL STRENGTHS")
        for s in strengths:
            st.markdown(f"<div class='good-card'><b>ANALYSIS:</b> {s}</div>", unsafe_allow_html=True)

    # 🚨 Fatal Flaw
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.subheader("🚨 THE FATAL FLAW")
        st.markdown(f"""
            <div class='flaw-card'>
                <h4 style='color:#f85149; margin-top:0;'>⚠️ [{f.get('severity')}] {f.get('issue')}</h4>
                <h5 style='color:#ff7b72; margin-top:15px;'>💥 CATASTROPHIC IMPACT:</h5>
                <p><i>"{f.get('catastrophic_impact')}"</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        # 🔒 The Paywall
        st.subheader("🧬 THE SINGLE PATH (REMEDIATION)")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='locked-cure-box'>
                    <h3 style='margin:0; color:#e3b341;'>🔒 THE CURE IS ENCRYPTED</h3>
                    <p style='color:#8b949e; margin-top:10px;'>Remediation code is restricted to Enterprise users.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Native Buy Button
            st.link_button("👉 SECURE ENTERPRISE PASS ($9) TO UNLOCK", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            st.write("")
            passcode = st.text_input("ENTER PASSCODE:", type="password")
            if st.button("🔓 VERIFY & DEPLOY SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Passcode. Access Denied.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.markdown(f"<div class='unlocked-cure'><h3>🟢 TECHNICAL SOLUTION</h3><p style='font-family: \"Fira Code\", monospace;'>{f.get('the_cure')}</p></div>", unsafe_allow_html=True)

    if st.button("🔄 CLEAR SCAN"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#484f58; font-size:10px; margin-top:100px; letter-spacing:3px;'>POWERED BY WAT SYSTEMS | AEGIS v11.4 | AUTHORITY LEVEL: SUPREME</div>", unsafe_allow_html=True)
