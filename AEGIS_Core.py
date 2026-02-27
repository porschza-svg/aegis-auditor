import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & GLOBAL UI CLOAKING
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Universal Logic Auditor", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    [data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    
    /* 💎 BRANDING */
    .hero-container { text-align: center; padding: 20px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 5px; font-weight: 900; margin-bottom: 0px; text-shadow: 0 0 30px rgba(88, 166, 255, 0.4); }
    .subtitle { color: #8b949e; font-size: 14px; letter-spacing: 2px; margin-bottom: 30px; }

    /* ⚡ 3-COLUMN DEEP INTELLIGENCE GRID */
    .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 25px; }
    .feature-card { background: rgba(22, 27, 34, 0.4); border: 1px solid #30363d; padding: 15px; border-radius: 12px; transition: 0.3s; backdrop-filter: blur(8px); min-height: 100px; cursor: pointer; }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-3px); background: rgba(31, 111, 235, 0.05); }
    .feature-title { color: #58a6ff; font-weight: 800; font-size: 11px; margin-bottom: 5px; text-transform: uppercase; }
    .feature-desc { color: #8b949e; font-size: 10.5px; line-height: 1.4; }
    .music-glow { border-color: #e3b341 !important; }

    /* 📘 EXPANDED MANUAL */
    .guide-box { background: #161b22; border-radius: 10px; padding: 20px; border: 1px solid #30363d; }
    .example-code { background: #0d1117; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 12px; color: #7ee787; margin-top: 10px; }

    /* 📥 INPUT & BUTTONS */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; font-family: 'Fira Code', monospace; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 16px; font-weight: 800; padding: 15px; border-radius: 12px; border: none; box-shadow: 0 4px 20px rgba(31, 111, 235, 0.3); }
    
    /* 📈 METRICS */
    .metric-box { background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); padding: 35px; border-radius: 20px; border: 1px solid #30363d; text-align: center; margin: 35px 0; }
    .custom-footer { text-align: center; color: #484f58; font-size: 11px; margin-top: 80px; padding-bottom: 30px; border-top: 1px solid #21262d; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL AUDITOR ENGINE (Final Version)
# ────────────────────────────────────────────────
def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS, the Universal Logic Auditor. Analyze for 3 critical logic flaws in Code, Business, or Music. Output JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"},
                {"role": "user", "content": payload[:15000]}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Logic Sync Fault.", "severity": "Critical", "remediation": "Validate payload/secrets."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        sys_msg = f"You are AEGIS Global Consultant. Payload: {original_payload[:5000]}. Findings: {json.dumps(scan_results)}. Provide step-by-step remediation."
        msgs = [{"role": "system", "content": sys_msg}]
        for m in st.session_state.chat_history: msgs.append(m)
        msgs.append({"role": "user", "content": user_input})
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=0.5)
        return resp.choices[0].message.content
    except: return "⚠️ Sync interrupted."

# ────────────────────────────────────────────────
# 3. GLOBAL MEMORY
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ────────────────────────────────────────────────
# 4. FINAL MARKET-READY DASHBOARD
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>🛡️ AEGIS</h1><p class='subtitle'>UNIVERSAL LOGIC & EXECUTION GUARANTY</p></div>", unsafe_allow_html=True)

# ⚡ CAPABILITY POP-OVER GRID (The "Deep Intelligence" Update)
col1, col2, col3 = st.columns(3)
with col1:
    with st.popover("💻 CODE SECURITY"):
        st.markdown("**Logic Bombs & API Audit**\nDetect hidden flaws and data leaks in your enterprise source code.")
    with st.popover("🎵 SETLIST LOGIC"):
        st.markdown("**Emotional Arc Engineering**\nOptimize energy curve and key transitions for high-impact live shows.")
with col2:
    with st.popover("🤖 WORKFLOW LOGIC"):
        st.markdown("**Agent Integrity Audit**\nIdentify deadlocks and logic loops in B2B AI automations.")
    with st.popover("🎸 SONG STRUCTURE"):
        st.markdown("**Hit Density Theory**\nAnalyze hook frequency and chord flow against global success patterns.")
with col3:
    with st.popover("🔗 SMART CONTRACTS"):
        st.markdown("**Exploit Analysis**\nAudit Reentrancy and Logic flaws in Solidity/Rust contracts.")
    with st.popover("⚖️ LEGAL ASSETS"):
        st.markdown("**Liability Loop Detection**\nScan NDAs and contracts for hidden risks and legal traps.")

# 📖 FINAL MANUAL
with st.expander("📖 OPERATIONAL MANUAL & EXPERT ADVICE"):
    t1, t2 = st.tabs(["🚀 Tech & Business", "🎸 Music & Arts"])
    with t1:
        st.write("1. **Paste Source/Logic** in the Payload box.")
        st.write("2. **Execute Audit** to reveal the Trust Score.")
        st.write("3. **Unlock Premium** to see all critical vulnerabilities.")
    with t2:
        st.write("1. **Paste Setlist** (Titles + Key/BPM) or Chord Progression.")
        st.write("2. **Execute Audit** to optimize show flow or song structure.")

payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste code, business logic, or music assets...")

if st.button("🚀 INITIATE GLOBAL AUDIT"):
    if not payload.strip(): st.error("❌ ERROR: Payload is empty.")
    else:
        with st.spinner("Executing Logic Audit..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False 
            st.session_state.chat_history = []
            st.rerun()

# ────────────────────────────────────────────────
# 5. RESULTS & REVENUE GATEWAY
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown(f"<div class='metric-box'><h3>Global Trust Score</h3><h1 style='font-size: 70px; color:#58a6ff;'>{res.get('trust_score', 0)}%</h1></div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Logic Matrix")
        st.error(f"**[{findings[0].get('severity')}]:** {findings[0].get('issue')}\n\n*Solution: {findings[0].get('remediation')}*")
        
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ FULL ACCESS GRANTED")
                for i in range(1, len(findings)):
                    with st.expander(f"[{findings[i].get('severity')}] {findings[i].get('issue')}", expanded=True):
                        st.write(findings[i].get('remediation'))
                
                # Chat with Consultant...
                if prompt := st.chat_input("Ask about your audit..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    reply = chat_with_consultant(prompt, payload, findings)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
            else:
                st.markdown(f"<div style='background:rgba(227,179,65,0.1); border:1px dashed #e3b341; padding:25px; border-radius:12px; text-align:center; color:#e3b341;'>🔒 <b>{len(findings)-1} INSIGHTS HIDDEN</b><br>Unlock the Full Intelligence Matrix ($9).</div>", unsafe_allow_html=True)
                u_code = st.text_input("PREMIUM PASSCODE:", type="password")
                if st.button("🔓 UNLOCK MATRIX"):
                    if u_code == st.secrets["AEGIS_PASSCODE"]:
                        st.session_state.unlocked = True
                        st.rerun()
                st.markdown("[👉 **Get Premium Pass ($9)**](https://porschza.gumroad.com/l/AEGIS)")

st.markdown("<div class='custom-footer'>AEGIS v8.0 | Sovereignty Edition | Secured by Enterprise Trust Layer</div>", unsafe_allow_html=True)
