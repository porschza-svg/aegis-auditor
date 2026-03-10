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
    .score-display { background: #0d1117; padding: 40px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 30px 0; border-top: 5px solid #58a6ff; }
    .good-card { background: rgba(46, 160, 67, 0.08); border-left: 4px solid #2ea043; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .flaw-card { background: rgba(248, 81, 73, 0.08); border-left: 4px solid #f85149; padding: 25px; border-radius: 8px; margin-bottom: 25px; border-right: 1px solid #30363d; border-top: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .locked-cure-box { background: repeating-linear-gradient( 45deg, rgba(227, 179, 65, 0.03), rgba(227, 179, 65, 0.03) 10px, rgba(0,0,0,0) 10px, rgba(0,0,0,0) 20px ); border: 1px dashed #e3b341; padding: 40px; border-radius: 16px; text-align: center; margin-bottom: 20px; }
    .unlocked-cure { background: rgba(46, 160, 67, 0.1); border: 1px solid #2ea043; padding: 30px; border-radius: 16px; color: #e6edf3; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. SUPREME AUDIT ENGINE (CLAUDE 3.5 SONNET)
# ────────────────────────────────────────────────
def run_aegis_audit(payload):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Missing API Key", "severity": "Critical", "catastrophic_impact": "System cannot link to neural core.", "the_cure": "Add ANTHROPIC_API_KEY in Secrets."}]}
        
        client = anthropic.Anthropic(api_key=api_key)
        system_prompt = (
            "You are AEGIS, a brutal, elite Universal Logic Auditor by WAT SYSTEMS. "
            "Analyze the payload strictly. Output JSON ONLY format: "
            "{"
            "  \"trust_score\": int, \"strengths\": [\"str\"], "
            "  \"findings\": [{\"issue\": \"str\", \"severity\": \"Critical\", \"catastrophic_impact\": \"str\", \"the_cure\": \"str\"}] "
            "}"
            "Respond ONLY with valid JSON."
        )
        
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=2500,
            temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": f"PAYLOAD:\n{payload[:12000]}"}]
        )
        
        raw_content = message.content[0].text.strip()
        
        # Clean potential markdown wrapping
        if "```json" in raw_content:
            raw_content = raw_content.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_content:
            raw_content = raw_content.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw_content)
    except Exception as e:
        return {"trust_score": 0, "strengths": [], "findings": [{"issue": "Uplink Error", "severity": "Critical", "catastrophic_impact": str(e), "the_cure": "Check API Credits or Key validity."}]}

# ────────────────────────────────────────────────
# 3. UI ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>AEGIS</h1><div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)

# Specialist Matrix (Static Preview)
col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("💻 CODE SECURITY"): st.caption("Audit logic bombs.")
with col2:
    with st.expander("🤖 WORKFLOW LOGIC"): st.caption("Solve B2B loops.")
with col3:
    with st.expander("🔗 SMART CONTRACTS"): st.caption("Web3 Exploit Shield.")

payload = st.text_area("TARGET PAYLOAD:", height=200, placeholder="Paste code or business logic for deep-intelligence audit...")

if st.button("🚀 INITIATE GLOBAL SCAN (FREE)"):
    if not payload.strip():
        st.error("❌ ERROR: No payload detected.")
    else:
        with st.spinner("Analyzing structural integrity..."):
            st.session_state.result = run_aegis_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 4. RESULTS & NATIVE BUTTONS (VIRAL & PAYWALL)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    score = res.get('trust_score', 0)
    
    st.markdown("---")
    
    # Global Trust Score Display
    st.markdown(f"""
        <div class='score-display'>
            <h3>GLOBAL TRUST SCORE</h3>
            <h1 style='font-size: 80px; color:#58a6ff; margin:0;'>{score}%</h1>
            <p style='color:#8b949e;'>Universal Logic Standard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 𝕏 Share Button (Native & Clickable)
    site_url = "https://aegis-auditor-rdztzsskvkrgaefesuzynl.streamlit.app/"
    tweet_text = f"My logic scored {score}% on AEGIS. God-tier architecture validated by WAT SYSTEMS. 🛡️🔥 Test yours: {site_url}"
    x_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
    st.link_button("𝕏 SHARE YOUR SCORE ON X", x_url, use_container_width=True)
    
    st.write("") # Spacer

    # ✅ Strengths Section
    strengths = res.get("strengths", [])
    if strengths:
        st.subheader("✅ STRUCTURAL STRENGTHS")
        for s in strengths:
            st.markdown(f"<div class='good-card'><b>DETECTED:</b> {s}</div>", unsafe_allow_html=True)

    # 🚨 Fatal Flaw Section
    findings = res.get("findings", [])
    if findings:
        f = findings[0]
        st.subheader("🚨 THE FATAL FLAW")
        st.markdown(f"""
            <div class='flaw-card'>
                <h4 style='color:#f85149; margin-top:0;'>⚠️ {f.get('issue')}</h4>
                <h5 style='color:#ff7b72;'>💥 CATASTROPHIC IMPACT:</h5>
                <p><i>"{f.get('catastrophic_impact')}"</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        # 🔒 Paywall Section
        st.subheader("🧬 THE SINGLE PATH (REMEDIATION)")
        if not st.session_state.unlocked:
            st.markdown("""
                <div class='locked-cure-box'>
                    <h3 style='margin:0; color:#e3b341;'>🔒 THE CURE IS LOCKED</h3>
                    <p style='color:#8b949e;'>Remediation code is restricted to Enterprise users.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Gumroad Buy Button (Native & Clickable)
            st.link_button("👉 SECURE ENTERPRISE PASS ($9) TO UNLOCK", "https://porschza.gumroad.com/l/AEGIS", type="primary", use_container_width=True)
            
            st.write("")
            passcode = st.text_input("ENTER PASSCODE:", type="password")
            if st.button("🔓 VERIFY & UNLOCK"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Passcode.")
        else:
            # Unlocked Cure Display
            st.markdown(f"""
                <div class='unlocked-cure'>
                    <h3 style='color:#3fb950; margin-top:0;'>🟢 SOLUTION UNLOCKED</h3>
                    <p>{f.get('the_cure')}</p>
                </div>
            """, unsafe_allow_html=True)

    if st.button("🔄 CLEAR SCAN"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#484f58; font-size:10px; margin-top:100px; letter-spacing:2px;'>POWERED BY WAT SYSTEMS | AEGIS v11.3</div>", unsafe_allow_html=True)
