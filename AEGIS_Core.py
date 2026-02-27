import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & GLOBAL UI CLOAKING
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Enterprise Security Scanner", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    /* 🛡️ CLOAK STREAMLIT UI (Global Level) */
    [data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 💎 PREMIUM GLOBAL STYLING */
    .main { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #58a6ff; text-align: center; text-transform: uppercase; letter-spacing: 2px; font-weight: 800;}
    
    /* Responsive Buttons */
    .stButton>button { width: 100%; background: linear-gradient(90deg, #1f6feb, #388bfd); color: white; font-size: 18px; font-weight: bold; padding: 12px; border-radius: 8px; border: none; box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4); transition: all 0.3s; }
    .stButton>button:hover { background: linear-gradient(90deg, #388bfd, #58a6ff); transform: translateY(-2px); }
    
    /* Metrics & Cards */
    .metric-box { background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; text-align: center; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); margin: 20px 0; }
    .locked-content { background: repeating-linear-gradient(45deg, #161b22, #161b22 10px, #0d1117 10px, #0d1117 20px); border: 1px dashed #e3b341; padding: 20px; border-radius: 8px; text-align: center; color: #e3b341; margin-top: 15px;}
    
    /* ⚡ CAPABILITY MATRIX (Optimized for Mobile) */
    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; margin-top: 10px; }
    .feature-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; transition: 0.3s; }
    .feature-card:hover { border-color: #58a6ff; box-shadow: 0 0 10px rgba(88, 166, 255, 0.2); }
    .feature-title { color: #58a6ff; font-weight: bold; font-size: 15px; margin-bottom: 5px; }
    .feature-desc { color: #8b949e; font-size: 12.5px; line-height: 1.4; }
    
    /* 💬 CHAT UI CLEANUP */
    .chat-container { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-top: 30px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); }
    .custom-footer { text-align: center; color: #8b949e; font-size: 11px; margin-top: 50px; opacity: 0.6; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL ENGINES (Scanner & Professional Consultant)
# ────────────────────────────────────────────────
AUDITOR_PROMPT = """
You are AEGIS, an elite security and logic auditor. Analyze the payload. 
Identify at least 3 critical vulnerabilities, logical flaws, or areas for improvement.
Output ONLY valid JSON:
{
  "trust_score": <int 0-100>,
  "findings": [
    {"issue": "<Punchy description>", "severity": "<Critical/Warning/Info>", "remediation": "<Actionable fix>"}
  ]
}
"""

def run_audit(payload):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": AUDITOR_PROMPT},
                {"role": "user", "content": f"Scan this (Priority Analysis):\n\n{payload[:15000]}"} # 🚀 Expanded Payload
            ],
            temperature=0.0,
            max_tokens=800,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {"trust_score": 0, "findings": [{"issue": "Secure Link Error.", "severity": "Critical", "remediation": "Check AEGIS configuration."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        
        # 🧠 Full Context Integration for Global Scaling
        system_context = f"You are AEGIS, the Global Enterprise Security Consultant. The user has unlocked the full report. \n\nTarget Payload: {original_payload[:5000]}\n\nIdentified Risks: {json.dumps(scan_results)}"
        
        messages = [{"role": "system", "content": system_context}]
        for msg in st.session_state.chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception:
        return "⚠️ Sync failed. Re-initialize secure connection."

# ────────────────────────────────────────────────
# 3. GLOBAL MEMORY SYSTEM
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state:
    st.session_state.scanned = False
    st.session_state.result = None
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ────────────────────────────────────────────────
# 4. DASHBOARD (Global Value Proposition)
# ────────────────────────────────────────────────
st.title("🛡️ AEGIS")
st.markdown("<p style='text-align:center; color:#8b949e; font-size: 16px;'>Enterprise-Grade Execution Guaranty System</p>", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-title">💻 Source Code & Security</div>
        <div class="feature-desc">Python, JS, C++ & API security audit.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🤖 B2B Workflow Logic</div>
        <div class="feature-desc">Audit AI automation & logic flows.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🔗 Smart Contracts</div>
        <div class="feature-desc">Solidity & Rust exploit detection.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">⚖️ Legal Contracts</div>
        <div class="feature-desc">NDA & business liability analysis.</div>
    </div>
</div>
""", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste your enterprise assets here for a global security scan...")

if st.button("🚀 INITIATE GLOBAL SCAN (Free Basic Report)"):
    if not payload.strip():
        st.error("❌ ERROR: Payload required.")
    else:
        progress_text = "Establishing Global Neural Link..."
        my_bar = st.progress(0, text=progress_text)
        time.sleep(0.4)
        my_bar.progress(60, text="Interrogating logic across clusters...")
        st.session_state.result = run_audit(payload)
        st.session_state.scanned = True
        st.session_state.unlocked = False 
        st.session_state.chat_history = []
        my_bar.progress(100, text="Scan Complete.")
        time.sleep(0.3)
        my_bar.empty()

# ────────────────────────────────────────────────
# 5. ENTERPRISE GATEWAY & CONSULTANT
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric("Global Trust Score", f"{res.get('trust_score', 0)} / 100")
    st.markdown("</div>", unsafe_allow_html=True)

    findings = res.get("findings", [])
    if len(findings) > 0:
        st.subheader("🚨 Threat Matrix")
        f0 = findings[0]
        st.error(f"**[{f0.get('severity')}]:** {f0.get('issue')}\n\n*Solution: {f0.get('remediation')}*")
        
        if len(findings) > 1:
            hidden = len(findings) - 1
            if st.session_state.unlocked:
                st.success("✅ Enterprise Access Granted:")
                for i in range(1, len(findings)):
                    item = findings[i]
                    if item.get('severity') == 'Critical': st.error(f"**[CRITICAL]:** {item.get('issue')}\n\n*Fix: {item.get('remediation')}*")
                    elif item.get('severity') == 'Warning': st.warning(f"**[WARNING]:** {item.get('issue')}\n\n*Fix: {item.get('remediation')}*")
                    else: st.info(f"**[INFO]:** {item.get('issue')}\n\n*Fix: {item.get('remediation')}*")
                
                # 💬 CONSULTANT INTERFACE
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                st.subheader("💬 AI Consultant")
                for m in st.session_state.chat_history:
                    with st.chat_message(m["role"]): st.markdown(m["content"])
                if prompt := st.chat_input("Ask AEGIS about your audit..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"): st.markdown(prompt)
                    with st.chat_message("assistant"):
                        reply = chat_with_consultant(prompt, payload, findings)
                        st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='locked-content'>🔒 <b>{hidden} Threats Hidden</b><br>Upgrade to reveal the Full Matrix and unlock the Interactive Consultant.</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🔑 Global Passcode")
                u_code = st.text_input("Enter your Premium Passcode:", placeholder="AEGIS-XXXX-XXXX", type="password")
                if st.button("🔓 UNLOCK ENTERPRISE"):
                    # 🔒 ดึงรหัสผ่านจาก Secrets เพื่อความปลอดภัยระดับโลก
                    if u_code == st.secrets["AEGIS_PASSCODE"]:
                        st.session_state.unlocked = True
                        st.rerun()
                    else:
                        st.error("❌ Access Denied.")
                st.markdown("[👉 **Get Premium Pass ($9)**](https://porschza.gumroad.com/l/AEGIS)")
    else:
        st.success("✅ Asset cleared by AEGIS Neural Scan.")

st.markdown("<div class='custom-footer'>AEGIS v7.1 | Global Scaling Edition | Enterprise Trust Layer</div>", unsafe_allow_html=True)
