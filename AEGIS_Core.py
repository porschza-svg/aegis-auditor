import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & HYPER-CLEAN UI
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Enterprise Security Scanner", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    /* 🛡️ CLOAK STREAMLIT UI */
    [data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 💎 GLOBAL HYPER-CLEAN STYLING */
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', -apple-system, sans-serif; }
    
    /* Header Animation */
    h1 { color: #ffffff; text-align: center; text-transform: uppercase; letter-spacing: 4px; font-weight: 900; margin-bottom: 5px; text-shadow: 0 0 20px rgba(88, 166, 255, 0.3); }
    .subtitle { text-align: center; color: #8b949e; font-size: 14px; margin-bottom: 40px; letter-spacing: 1px; }

    /* ⚡ REFINED CAPABILITY MATRIX */
    .feature-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-bottom: 35px; }
    .feature-card { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; padding: 18px; border-radius: 12px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); backdrop-filter: blur(10px); }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(31, 111, 235, 0.15); background: rgba(31, 111, 235, 0.05); }
    .feature-title { color: #58a6ff; font-weight: 700; font-size: 14px; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
    .feature-desc { color: #8b949e; font-size: 12px; line-height: 1.5; }

    /* 📥 UNIFIED INPUT CONTAINER */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; padding: 15px !important; transition: 0.3s; }
    .stTextArea textarea:focus { border-color: #58a6ff !important; box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2) !important; }

    /* 🚀 PREMIUM BUTTON */
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 16px; font-weight: 700; padding: 14px; border-radius: 12px; border: none; box-shadow: 0 4px 20px rgba(31, 111, 235, 0.3); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 8px 25px rgba(31, 111, 235, 0.5); }

    /* 📊 METRICS & CHAT */
    .metric-box { background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); padding: 30px; border-radius: 16px; border: 1px solid #30363d; text-align: center; margin: 30px 0; }
    .chat-container { background: #0d1117; border: 1px solid #30363d; border-radius: 16px; padding: 25px; margin-top: 35px; box-shadow: 0 20px 50px rgba(0,0,0,0.4); }
    .locked-content { background: #1c1502; border: 1px dashed #e3b341; padding: 25px; border-radius: 12px; text-align: center; color: #e3b341; font-weight: 600; margin-top: 20px; }
    .custom-footer { text-align: center; color: #484f58; font-size: 11px; margin-top: 60px; padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL ENGINES (Scanner & Consultant)
# ────────────────────────────────────────────────
def run_audit(payload):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS, an elite security auditor. Identify 3 critical logic/security flaws. Output JSON only: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"},
                {"role": "user", "content": payload[:15000]}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Audit Link Interrupted.", "severity": "Critical", "remediation": "Check system secrets."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_context = f"You are AEGIS Global Consultant. Payload: {original_payload[:5000]}. Findings: {json.dumps(scan_results)}"
        messages = [{"role": "system", "content": system_context}]
        for msg in st.session_state.chat_history: messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.4)
        return response.choices[0].message.content
    except: return "⚠️ Sync Error."

# ────────────────────────────────────────────────
# 3. GLOBAL MEMORY SYSTEM
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ────────────────────────────────────────────────
# 4. DASHBOARD (Hyper-Clean Layout)
# ────────────────────────────────────────────────
st.markdown("<h1>🛡️ AEGIS</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>ENTERPRISE-GRADE EXECUTION GUARANTY SYSTEM</p>", unsafe_allow_html=True)

# Modern 2x2 Grid for Desktop/Mobile
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-title">💻 Code & Security</div>
        <div class="feature-desc">Source audit for Python, JS & APIs.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🤖 Workflow Logic</div>
        <div class="feature-desc">AI automation & logic flaw detection.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🔗 Smart Contracts</div>
        <div class="feature-desc">Solidity & Rust exploit analysis.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">⚖️ Legal Assets</div>
        <div class="feature-desc">NDA & contract liability scan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste your enterprise assets here for a deep-intelligence scan...")

if st.button("🚀 INITIATE GLOBAL SCAN"):
    if not payload.strip():
        st.error("❌ Payload required.")
    else:
        with st.spinner("Establishing Neural Link..."):
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
    st.markdown(f"<div class='metric-box'><h3>Global Trust Score</h3><h1 style='font-size: 60px; color:#58a6ff;'>{res.get('trust_score', 0)}%</h1></div>", unsafe_allow_html=True)

    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Threat Matrix")
        st.error(f"**[{findings[0].get('severity')}]:** {findings[0].get('issue')}\n\n*Fix: {findings[0].get('remediation')}*")
        
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ Enterprise Access Granted:")
                for i in range(1, len(findings)):
                    item = findings[i]
                    with st.expander(f"[{item.get('severity')}] {item.get('issue')}", expanded=True):
                        st.write(f"**Actionable Fix:** {item.get('remediation')}")
                
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                st.subheader("💬 AI Consultant")
                for m in st.session_state.chat_history:
                    with st.chat_message(m["role"]): st.markdown(m["content"])
                if prompt := st.chat_input("Ask about your audit..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"): st.markdown(prompt)
                    with st.chat_message("assistant"):
                        reply = chat_with_consultant(prompt, payload, findings)
                        st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='locked-content'>🔒 {len(findings)-1} PRO THREATS DETECTED<br>Unlock the Full Matrix & AI Consultant Module.</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                u_code = st.text_input("ENTER PREMIUM PASSCODE:", type="password")
                if st.button("🔓 UNLOCK ENTERPRISE REPORT"):
                    if u_code == st.secrets["AEGIS_PASSCODE"]:
                        st.session_state.unlocked = True
                        st.rerun()
                    else: st.error("❌ Denied.")
                st.markdown("[👉 **Get Premium Pass ($9)**](https://porschza.gumroad.com/l/AEGIS)")

st.markdown("<div class='custom-footer'>AEGIS v7.2 | Hyper-Clean Edition | Secured by Enterprise Trust Layer</div>", unsafe_allow_html=True)
