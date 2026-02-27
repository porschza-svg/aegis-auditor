import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & GLOBAL UI
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Global Logic Auditor", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    [data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    h1 { color: #ffffff; text-align: center; text-transform: uppercase; letter-spacing: 5px; font-weight: 900; margin-bottom: 0px; text-shadow: 0 0 30px rgba(88, 166, 255, 0.4); }
    .subtitle { text-align: center; color: #8b949e; font-size: 14px; letter-spacing: 2px; margin-bottom: 30px; }
    
    /* ⚡ 3-COLUMN CAPABILITY GRID */
    .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 30px; }
    .feature-card { background: rgba(22, 27, 34, 0.4); border: 1px solid #30363d; padding: 15px; border-radius: 12px; transition: 0.3s; backdrop-filter: blur(8px); min-height: 120px; }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-3px); }
    .feature-title { color: #58a6ff; font-weight: 800; font-size: 11px; margin-bottom: 5px; text-transform: uppercase; }
    .feature-desc { color: #8b949e; font-size: 10.5px; line-height: 1.4; }
    .music-glow { border-color: #e3b341 !important; box-shadow: 0 0 10px rgba(227, 179, 65, 0.1); }

    /* 📘 EXPANDED INSTRUCTION DESIGN */
    .step-box { background: #161b22; border-radius: 10px; padding: 20px; border: 1px solid #30363d; margin-top: 10px; }
    .step-number { background: #1f6feb; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 10px; }
    .example-code { background: #0d1117; padding: 10px; border-radius: 6px; border: 1px solid #21262d; font-family: monospace; font-size: 12px; color: #7ee787; margin-top: 10px; }

    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; padding: 18px !important; font-family: 'Fira Code', monospace; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 16px; font-weight: 800; padding: 15px; border-radius: 12px; border: none; box-shadow: 0 4px 20px rgba(31, 111, 235, 0.3); }
    .custom-footer { text-align: center; color: #484f58; font-size: 11px; margin-top: 80px; padding-bottom: 30px; border-top: 1px solid #21262d; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# (Neural Engines run_audit and chat_with_consultant remain the same as v7.4)
def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS, the Universal Logic Auditor. Analyze for 3 critical logic/security flaws. If it's music, analyze energy/flow. Output JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"},
                {"role": "user", "content": payload[:15000]}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Logic Link Fault.", "severity": "Critical", "remediation": "Check secrets."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        sys_msg = f"You are AEGIS Expert Consultant. Payload: {original_payload[:5000]}. Vulnerabilities: {json.dumps(scan_results)}. Guide the user step-by-step."
        msgs = [{"role": "system", "content": sys_msg}]
        for m in st.session_state.chat_history: msgs.append(m)
        msgs.append({"role": "user", "content": user_input})
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=0.5)
        return resp.choices[0].message.content
    except: return "⚠️ Sync interrupted."

if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

st.markdown("<h1>🛡️ AEGIS</h1><p class='subtitle'>UNIVERSAL LOGIC & EXECUTION GUARANTY</p>", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card"><div class="feature-title">💻 Code Security</div><div class="feature-desc">Source audit for Python, JS & APIs.</div></div>
    <div class="feature-card"><div class="feature-title">🤖 Workflow Logic</div><div class="feature-desc">AI automation & business flow audit.</div></div>
    <div class="feature-card"><div class="feature-title">🔗 Smart Contracts</div><div class="feature-desc">Solidity & Rust exploit analysis.</div></div>
    <div class="feature-card music-glow"><div class="feature-title">🎵 Setlist Logic</div><div class="feature-desc">Energy curve & transition audit.</div></div>
    <div class="feature-card music-glow"><div class="feature-title">🎸 Song Structure</div><div class="feature-desc">Analyze chord flow & hit-potential.</div></div>
    <div class="feature-card"><div class="feature-title">⚖️ Legal Assets</div><div class="feature-desc">NDA & contract liability scan.</div></div>
</div>
""", unsafe_allow_html=True)

# 📘 NEW: INTERACTIVE OPERATIONAL MANUAL (v7.5)
with st.expander("📖 OPERATIONAL MANUAL: HOW TO USE AEGIS"):
    tab1, tab2 = st.tabs(["💻 For Tech & Business", "🎵 For Musicians & Shows"])
    
    with tab1:
        st.markdown("""
        <div class="step-box">
            <b>1. Copy Code/Logic:</b> Grab your source code or business workflow description.<br>
            <b>2. Paste:</b> Put it in the 'Target Payload' box below.<br>
            <b>3. Scan:</b> Click 'Initiate Logic Audit'.<br><br>
            <i>Example Payload:</i>
            <div class="example-code">def transfer(amount):<br>&nbsp;&nbsp;user.balance -= amount<br>&nbsp;&nbsp;db.save(user) # Check for Race Conditions!</div>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="step-box">
            <b>1. Prepare Setlist:</b> List your songs with Key and BPM (optional but recommended).<br>
            <b>2. Paste:</b> Put the list or your song's chord progression below.<br>
            <b>3. Scan:</b> AEGIS will audit your show's energy flow or songwriting logic.<br><br>
            <i>Example Payload:</i>
            <div class="example-code">1. Song A - Key: G (BPM: 120)<br>2. Song B - Key: Eb (BPM: 145)<br>3. Song C - Key: G (BPM: 110)</div>
        </div>
        """, unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste your data here for a deep-intelligence scan...")

if st.button("🚀 INITIATE LOGIC AUDIT"):
    if not payload.strip(): st.error("❌ ERROR: Payload is empty.")
    else:
        with st.spinner("Analyzing..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False 
            st.session_state.chat_history = []
            st.rerun()

# (Results & Premium Gateway logic same as v7.4)
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown(f"<div style='text-align:center;'><h3>Global Trust Score</h3><h1 style='font-size: 70px; color:#58a6ff;'>{res.get('trust_score', 0)}%</h1></div>", unsafe_allow_html=True)
    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Logic Matrix")
        st.error(f"**[{findings[0].get('severity')}]:** {findings[0].get('issue')}\n\n*Advice: {findings[0].get('remediation')}*")
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ Full Access Granted:")
                for i in range(1, len(findings)):
                    with st.expander(f"[{findings[i].get('severity')}] {findings[i].get('issue')}", expanded=True):
                        st.write(findings[i].get('remediation'))
                # Chat consultant module...
                if prompt := st.chat_input("Ask AEGIS..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    reply = chat_with_consultant(prompt, payload, findings)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
            else:
                st.markdown(f"<div class='locked-content'>🔒 <b>{len(findings)-1} INSIGHTS HIDDEN</b><br>Unlock Premium to reveal full audit & AI Consultant.</div>", unsafe_allow_html=True)
                u_code = st.text_input("ENTER PREMIUM PASSCODE:", type="password")
                if st.button("🔓 UNLOCK"):
                    if u_code == st.secrets["AEGIS_PASSCODE"]:
                        st.session_state.unlocked = True
                        st.rerun()
                st.markdown("[👉 **Get Premium Pass ($9)**](https://porschza.gumroad.com/l/AEGIS)")

st.markdown("<div class='custom-footer'>AEGIS v7.5 | Operational Excellence Edition</div>", unsafe_allow_html=True)
