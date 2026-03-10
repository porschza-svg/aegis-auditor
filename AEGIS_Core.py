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
    .hero-container { text-align: center; padding: 40px 0 10px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 12px; font-weight: 900; margin-bottom: 5px; text-shadow: 0 0 50px rgba(88, 166, 255, 0.4); font-size: 3rem; }
    .brand-tag { color: #58a6ff; font-size: 12px; letter-spacing: 5px; font-weight: 800; margin-bottom: 40px; text-transform: uppercase; }
    .uplink-box { background: rgba(31, 111, 235, 0.05); border: 1px dashed #388bfd; border-radius: 16px; padding: 20px; margin-bottom: 25px; text-align: center; }
    div[data-testid="stExpander"] { background: rgba(22, 27, 34, 0.5); border: 1px solid #30363d !important; border-radius: 12px !important; }
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; font-family: 'Fira Code', monospace; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-weight: 900; padding: 18px; border-radius: 12px; border: none; letter-spacing: 2px; }
    .score-display { background: #0d1117; padding: 40px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 30px 0; border-top: 5px solid #58a6ff; }
    .good-card { background: rgba(46, 160, 67, 0.08); border: 1px solid #2ea043; padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 4px solid #2ea043; }
    .flaw-card { background: rgba(248, 81, 73, 0.08); border: 1px solid #f85149; padding: 25px; border-radius: 12px; margin-bottom: 25px; border-left: 4px solid #f85149; }
    .locked-cure { background: repeating-linear-gradient( 45deg, rgba(227, 179, 65, 0.05), rgba(227, 179, 65, 0.05) 10px, rgba(0,0,0,0.2) 10px, rgba(0,0,0,0.2) 20px ); border: 1px solid #e3b341; padding: 40px; border-radius: 16px; text-align: center; color: #e3b341; }
    .unlocked-cure { background: rgba(46, 160, 67, 0.1); border: 1px solid #2ea043; padding: 30px; border-radius: 16px; color: #e6edf3; margin-bottom: 20px; }
    .share-btn { display: inline-block; width: 100%; text-align: center; background: #ffffff; color: #000000 !important; padding: 15px; border-radius: 12px; font-weight: 900; text-decoration: none; margin-top: 15px; transition: 0.3s; font-family: 'Inter', sans-serif; letter-spacing: 1px; border: none; }
    .share-btn:hover { background: #cccccc; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. SUPREME AUDIT ENGINE (THE VIRAL CURE PROTOCOL)
# ────────────────────────────────────────────────
def run_aegis_audit(payload, audio_meta=None):
    try:
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        audio_context = f" [AUDIO_UPLINK_METADATA: {audio_meta}]" if audio_meta else ""
        
        system_prompt = (
            "You are AEGIS, a brutal, elite Universal Logic Auditor by WAT SYSTEMS. "
            "Analyze the payload strictly. Output JSON ONLY format: "
            "{"
            "  \"trust_score\": int (0-100 based on structural integrity), "
            "  \"strengths\": [\"point 1\", \"point 2\"], "
            "  \"findings\": ["
            "      {"
            "          \"issue\": \"Name of the vulnerability or flaw\", "
            "          \"severity\": \"Critical or High\", "
            "          \"catastrophic_impact\": \"Describe exactly how this flaw will destroy the project/business if deployed. Be brutal and realistic.\", "
            "          \"the_cure\": \"The exact, step-by-step technical fix or code snippet to resolve it.\" "
            "      }"
            "  ]"
            "}"
            "Be brutally honest. No fluff. Respond ONLY with valid JSON."
        )
        
        message = client.messages.create(
            model="claude-3-5-sonnet-latest", 
            max_tokens=2500,
            temperature=0.0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"PAYLOAD:\n{payload[:12000]}{audio_context}\n\nRespond ONLY with valid JSON. Do not include markdown formatting like ```json."}
            ]
        )
        
        raw_content = message.content[0].text.strip()
        
        # Clean JSON if AI wraps it in markdown
        if raw_content.startswith("```json"):
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif raw_content.startswith("```"):
            raw_content = raw_content.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_content)
    except Exception as e: 
        return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Uplink Error.", "severity": "Critical", "catastrophic_impact": str(e), "the_cure": "Verify API Key & Billing."}]}

# ────────────────────────────────────────────────
# 3. DASHBOARD ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("""
    <div class='hero-container'>
        <h1>AEGIS</h1>
        <div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align:center; color:#238636; font-size:10px; font-weight:800; letter-spacing:2px; margin-bottom:20px;'>
        ● OBJECTIVE ENGINE: ONLINE (STATE-OF-THE-ART)
    </div>
""", unsafe_allow_html=True)

# 🌐 SPECIALIST MATRIX
col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("💻 CODE SECURITY"): st.caption("Audit logic bombs.")
    with st.expander("🎵 SETLIST LOGIC"): st.caption("Energy curve audit.")
with col2:
    with st.expander("🤖 WORKFLOW LOGIC"): st.caption("Solve B2B loops.")
    with st.expander("🎸 SONG STRUCTURE"): st.caption("Hook density audit.")
with col3:
    with st.expander("🔗 SMART CONTRACTS"): st.caption("Web3 Exploit Shield.")
    with st.expander("⚖️ LEGAL ASSETS"): st.caption("Scan liability loops.")

# 🛰️ AUDIO-NEURAL UPLINK
st.markdown("""
    <div class='uplink-box'>
        <span style='color:#388bfd; font-size:12px; font-weight:800; letter-spacing:2px;'>
            🛰️ SOVEREIGN AUDIO UPLINK
        </span>
    </div>
""", unsafe_allow_html=True)

audio_file = st.file_uploader("Upload musical payload", type=['mp3', 'wav'], label_visibility="collapsed")
if audio_file:
    st.success(f"Uplink Established: {audio_file.name}")

# 📥 PAYLOAD INPUT
payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste code, business logic, or structural plans for a neutral, objective audit...")

if st.button("🚀 INITIATE GLOBAL SCAN (FREE)"):
    if not payload.strip() and not audio_file:
        st.error("❌ ERROR: No payload detected.")
    else:
        with st.spinner("Extracting structural truth..."):
            audio_info = f"File: {audio_file.name}, Size: {audio_file.size} bytes" if audio_file else None
            st.session_state.result = run_aegis_audit(payload, audio_info)
            
            # 📡 ---- TELEGRAM RADAR ----
            try:
                score = st.session_state.result.get('trust_score', 0)
                bot_token = st.secrets.get("TELEGRAM_BOT_TOKEN", "")
                chat_id = st.secrets.get("TELEGRAM_CHAT_ID", "")
                if bot_token and chat_id:
                    msg = f"🚨 [AEGIS RADAR] มีคนกำลังสแกนระบบ!\n🛡️ Trust Score: {score}%"
                    requests.post(f"[https://api.telegram.org/bot](https://api.telegram.org/bot){bot_token}/sendMessage", data={"chat_id": chat_id, "text": msg})
            except Exception: pass
            
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 4. RESULTS & VIRAL CURE PROTOCOL
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    
    score = res.get('trust_score', 0)
    
    st.markdown(f"""
        <div class='score-display'>
            <h3>GLOBAL TRUST SCORE</h3>
            <h1 style='font-size: 80px; color:#58a6ff; margin:0;'>{score}%</h1>
            <p style='color:#8b949e;'>Universal Logic Standard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- VIRAL TRIGGER: SHARE TO X ---
    site_url = "[https://aegis-auditor-rdztzsskvkrgaefesuzynl.streamlit.app/](https://aegis-auditor-rdztzsskvkrgaefesuzynl.streamlit.app/)" 
    if score >= 85:
        tweet_text = f"My structural logic scored {score}% on AEGIS. God-tier architecture validated by WAT SYSTEMS. 🛡️🔥 Test your own payload before you deploy blind: {site_url}"
    else:
        tweet_text = f"AEGIS just brutally audited my logic layer. Trust score: {score}%. The structural flaw it found is a ticking time bomb. 🚨 Test your own payload: {site_url}"
    
    encoded_tweet = urllib.parse.quote(tweet_text)
    x_share_url = f"[https://twitter.com/intent/tweet?text=](https://twitter.com/intent/tweet?text=){encoded_tweet}"
    
    st.markdown(f"""
        <a href="{x_share_url}" target="_blank" class="share-btn">
            𝕏 SHARE YOUR SCORE ON X
        </a>
        <br><br>
    """, unsafe_allow_html=True)
    
    # ✅ THE GOOD (Strengths)
    strengths = res.get("strengths", [])
    if strengths:
        st.markdown("### ✅ THE STRUCTURAL TRUTH (Strengths)")
        for s in strengths:
            st.markdown(f"<div class='good-card'><b>DETECTED:</b> {s}</div>", unsafe_allow_html=True)

    # 🔥 THE FLAW (Catastrophic Impact)
    findings = res.get("findings", [])
    if findings:
        primary_flaw = findings[0]
        st.markdown("### 🚨 THE FATAL FLAW (CRITICAL RISK)")
        st.markdown(f"""
            <div class='flaw-card'>
                <h4 style='color:#f85149; margin-top:0;'>⚠️ [{primary_flaw.get('severity')}] {primary_flaw.get('issue')}</h4>
                <h5 style='color:#ff7b72; margin-top:15px;'>💥 CATASTROPHIC IMPACT:</h5>
                <p><i>"{primary_flaw.get('catastrophic_impact')}"</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        # 🔒 THE CURE PAYWALL
        st.markdown("### 🧬 THE SINGLE PATH (REMEDIATION)")
        if not st.session_state.unlocked:
            st.markdown(f"""
                <div class='locked-cure'>
                    <h3 style='margin:0;'>🔒 THE CURE IS LOCKED</h3>
                    <p style='color:#8b949e;'>The exact code/solution to patch this vulnerability is restricted to Enterprise users.</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='text-align:center; margin-top:20px; margin-bottom:10px;'>
                    <a href='[https://porschza.gumroad.com/l/AEGIS](https://porschza.gumroad.com/l/AEGIS)' target='_blank' style='background:#e3b341; color:#000; padding:12px 24px; border-radius:8px; font-weight:900; text-decoration:none;'>
                        👉 SECURE ENTERPRISE PASS ($9) TO UNLOCK
                    </a>
                </div>
            """, unsafe_allow_html=True)
            
            passcode = st.text_input("ENTER PASSCODE:", type="password")
            if st.button("🔓 VERIFY & UNLOCK SOLUTION"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("❌ Access Denied.")
        else:
            # 🟢 UNLOCKED CONTENT
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            st.markdown(f"""
                <div class='unlocked-cure'>
                    <h3 style='color:#3fb950; margin-top:0;'>🟢 PRIMARY SOLUTION</h3>
                    <p>{primary_flaw.get('the_cure')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Show additional flaws if any
            if len(findings) > 1:
                st.markdown("#### 🔍 ADDITIONAL LOGIC GAPS")
                for i in range(1, len(findings)):
                    with st.expander(f"[{findings[i].get('severity')}] {findings[i].get('issue')}", expanded=True):
                        st.markdown(f"**Impact:** {findings[i].get('catastrophic_impact')}")
                        st.markdown(f"**The Cure:** {findings[i].get('the_cure')}")
    
    if st.button("🔄 CLEAR SCAN"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("""
    <div style='text-align:center; color:#484f58; font-size:10px; margin-top:100px; letter-spacing:2px;'>
        POWERED BY WAT SYSTEMS | AEGIS v11.2 (COMPLETE)
    </div>
""", unsafe_allow_html=True)
