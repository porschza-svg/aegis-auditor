import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & GLOBAL UI CLOAKING
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Global Enterprise Auditor", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    /* 🛡️ CLOAK STREAMLIT UI */
    [data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 💎 GLOBAL AUTHORITY STYLING */
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    
    /* Hero Section */
    .hero-container { text-align: center; padding: 20px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 5px; font-weight: 900; margin-bottom: 0px; text-shadow: 0 0 30px rgba(88, 166, 255, 0.4); }
    .subtitle { color: #8b949e; font-size: 14px; letter-spacing: 2px; margin-bottom: 30px; }

    /* ⚡ REFINED 2x2 GRID */
    .feature-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 30px; }
    .feature-card { background: rgba(22, 27, 34, 0.4); border: 1px solid #30363d; padding: 20px; border-radius: 12px; transition: 0.3s ease-in-out; backdrop-filter: blur(8px); }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-3px); background: rgba(31, 111, 235, 0.05); }
    .feature-title { color: #58a6ff; font-weight: 800; font-size: 14px; margin-bottom: 8px; text-transform: uppercase; }
    .feature-desc { color: #8b949e; font-size: 12px; line-height: 1.6; }

    /* 📖 USER GUIDE & ADVICE */
    .guide-box { background: #161b22; border-left: 4px solid #1f6feb; padding: 20px; border-radius: 8px; margin-bottom: 25px; }
    .advice-text { color: #e3b341; font-weight: 600; font-size: 13px; margin-bottom: 10px; }

    /* 📥 INPUT AREA */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; padding: 18px !important; font-family: 'Fira Code', monospace; }
    
    /* 🚀 ACTION BUTTON */
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 16px; font-weight: 800; padding: 15px; border-radius: 12px; border: none; box-shadow: 0 4px 20px rgba(31, 111, 235, 0.3); letter-spacing: 1px; }
    .stButton>button:hover { transform: scale(1.01); box-shadow: 0 8px 30px rgba(31, 111, 235, 0.5); }

    /* 📊 REPORT & CONSULTANT */
    .metric-box { background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); padding: 35px; border-radius: 20px; border: 1px solid #30363d; text-align: center; margin: 35px 0; }
    .chat-container { background: #0d1117; border: 1px solid #30363d; border-radius: 20px; padding: 25px; margin-top: 40px; }
    .locked-content { background: rgba(227, 179, 65, 0.05); border: 1px dashed #e3b341; padding: 30px; border-radius: 15px; text-align: center; color: #e3b341; margin-top: 25px; }
    .custom-footer { text-align: center; color: #484f58; font-size: 11px; margin-top: 80px; padding-bottom: 30px; border-top: 1px solid #21262d; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL ENGINES (Optimized for Global Scaling)
# ────────────────────────────────────────────────
def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS, the elite global logic auditor. Analyze for 3 critical flaws. Output ONLY JSON: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"},
                {"role": "user", "content": f"Scan this enterprise asset:\n\n{payload[:15000]}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Secure Link Fault.", "severity": "Critical", "remediation": "Validate API configuration."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_context = f"You are AEGIS Global Consultant. Payload Context: {original_payload[:5000]}. Vulnerabilities: {json.dumps(scan_results)}"
        messages = [{"role": "system", "content": system_context}]
        for msg in st.session_state.chat_history: messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.5)
        return response.choices[0].message.content
    except: return "⚠️ Sync interrupted."

# ────────────────────────────────────────────────
# 3. GLOBAL MEMORY SYSTEM
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ────────────────────────────────────────────────
# 4. DASHBOARD (Global Authority Layout)
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>🛡️ AEGIS</h1><p class='subtitle'>ENTERPRISE-GRADE EXECUTION GUARANTY SYSTEM</p></div>", unsafe_allow_html=True)

# 2x2 Capability Grid
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-title">💻 Code & Security</div>
        <div class="feature-desc">Source audit for Python, JavaScript, and APIs.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🤖 Workflow Logic</div>
        <div class="feature-desc">AI automation and logical business flow detection.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🔗 Smart Contracts</div>
        <div class="feature-desc">Solidity and Rust exploit and logic analysis.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">⚖️ Legal Assets</div>
        <div class="feature-desc">NDA, business contracts, and liability scanning.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 📖 NEW: USER GUIDE & EXPERT ADVICE
with st.expander("📖 HOW TO USE & EXPERT ADVICE (v7.3)"):
    st.markdown("""
    <div class="guide-box">
        <p class="advice-text">💡 ARCHITECT'S ADVICE:</p>
        <p style='font-size: 13px; color: #8b949e;'>
        AEGIS excels at detecting <b>hidden logic flaws</b> that standard syntax linters miss. 
        For the most accurate audit, provide the full context of your function or contract.
        </p>
        <hr style='border: 0.5px solid #30363d; margin: 15px 0;'>
        <p><b>Quick Start:</b></p>
        <ol style='font-size: 13px; color: #f0f6fc;'>
            <li>Paste your code or business logic into the <b>Target Payload</b> box.</li>
            <li>Click <b>Initiate Global Scan</b> to receive your free Trust Score.</li>
            <li>Unlock the <b>Premium Pass</b> to reveal the full Threat Matrix and chat with the AI Consultant.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste your enterprise assets here for a deep-intelligence scan (Max 15,000 chars)...")

if st.button("🚀 INITIATE GLOBAL SCAN"):
    if not payload.strip():
        st.error("❌ ERROR: Payload is empty. Please provide data to scan.")
    else:
        with st.spinner("Establishing Neural Connection..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False 
            st.session_state.chat_history = []
            st.rerun()

# ────────────────────────────────────────────────
# 5. RESULTS & PREMIUM GATEWAY
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown(f"<div class='metric-box'><h3>Global Trust Score</h3><h1 style='font-size: 70px; color:#58a6ff; margin:0;'>{res.get('trust_score', 0)}%</h1></div>", unsafe_allow_html=True)

    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Threat Matrix")
        # Show only 1st finding as free sample
        f0 = findings[0]
        st.error(f"**[{f0.get('severity')}]:** {f0.get('issue')}\n\n*Fix: {f0.get('remediation')}*")
        
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ Enterprise Access Granted:")
                for i in range(1, len(findings)):
                    item = findings[i]
                    with st.expander(f"[{item.get('severity')}] {item.get('issue')}", expanded=True):
                        st.write(f"**Remediation:** {item.get('remediation')}")
                
                # 💬 AI CONSULTANT MODULE
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                st.subheader("💬 AI Security Consultant")
                for m in st.session_state.chat_history:
                    with st.chat_message(m["role"]): st.markdown(m["content"])
                if prompt := st.chat_input("Ask AEGIS to help patch your vulnerabilities..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"): st.markdown(prompt)
                    with st.chat_message("assistant"):
                        reply = chat_with_consultant(prompt, payload, findings)
                        st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='locked-content'>🔒 <b>{len(findings)-1} ADDITIONAL THREATS HIDDEN</b><br>Upgrade to reveal the full audit and unlock the AI Consultant module.</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b = st.columns([2,1])
                with col_a:
                    u_code = st.text_input("ENTER PREMIUM PASSCODE:", type="password", placeholder="Paste your $9 Passcode here...")
                with col_b:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔓 UNLOCK"):
                        if u_code == st.secrets["AEGIS_PASSCODE"]:
                            st.session_state.unlocked = True
                            st.rerun()
                        else: st.error("Invalid Code.")
                st.markdown("[👉 **Get your Premium Pass instantly ($9)**](https://porschza.gumroad.com/l/AEGIS)")

st.markdown("<div class='custom-footer'>AEGIS v7.3 | Global Authority Edition | Secured by Enterprise Trust Layer</div>", unsafe_allow_html=True)
