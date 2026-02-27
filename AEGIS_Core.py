import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & ART-LOGIC UI
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Enterprise & Music Logic Auditor", layout="centered", page_icon="🛡️")

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

    /* ⚡ SYMMETRICAL 3-COLUMN GRID (v7.4) */
    .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 30px; }
    .feature-card { background: rgba(22, 27, 34, 0.4); border: 1px solid #30363d; padding: 15px; border-radius: 12px; transition: 0.3s ease-in-out; backdrop-filter: blur(8px); min-height: 120px; }
    .feature-card:hover { border-color: #58a6ff; transform: translateY(-3px); background: rgba(31, 111, 235, 0.05); }
    .feature-title { color: #58a6ff; font-weight: 800; font-size: 11px; margin-bottom: 5px; text-transform: uppercase; }
    .feature-desc { color: #8b949e; font-size: 10.5px; line-height: 1.4; }
    .music-glow { border-color: #e3b341 !important; box-shadow: 0 0 10px rgba(227, 179, 65, 0.2); }

    /* 📖 USER GUIDE */
    .guide-box { background: #161b22; border-left: 4px solid #1f6feb; padding: 20px; border-radius: 8px; margin-bottom: 25px; }

    /* 📥 INPUT AREA */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; padding: 18px !important; font-family: 'Fira Code', monospace; }
    
    /* 🚀 ACTION BUTTON */
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 16px; font-weight: 800; padding: 15px; border-radius: 12px; border: none; box-shadow: 0 4px 20px rgba(31, 111, 235, 0.3); letter-spacing: 1px; }

    /* 📊 REPORT & CONSULTANT */
    .metric-box { background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); padding: 35px; border-radius: 20px; border: 1px solid #30363d; text-align: center; margin: 35px 0; }
    .chat-container { background: #0d1117; border: 1px solid #30363d; border-radius: 20px; padding: 25px; margin-top: 40px; }
    .locked-content { background: rgba(227, 179, 65, 0.05); border: 1px dashed #e3b341; padding: 30px; border-radius: 15px; text-align: center; color: #e3b341; margin-top: 25px; }
    .custom-footer { text-align: center; color: #484f58; font-size: 11px; margin-top: 80px; padding-bottom: 30px; border-top: 1px solid #21262d; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL ENGINES (Unified Logic Auditor)
# ────────────────────────────────────────────────
AUDITOR_PROMPT = """
You are AEGIS, the Universal Logic Auditor. 
Your goal is to identify 'Logical Flaws' in the provided payload.
- If it's CODE: Find security and logic vulnerabilities.
- If it's a MUSIC SETLIST: Analyze energy curve, key transitions, and audience engagement flow.
- If it's a SONG STRUCTURE: Analyze chord progression logic, hook density, and structural integrity.

Output ONLY valid JSON:
{
  "trust_score": <int 0-100>,
  "findings": [
    {"issue": "<Description>", "severity": "<Critical/Warning/Info>", "remediation": "<Actionable fix>"}
  ]
}
"""

def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": AUDITOR_PROMPT},
                {"role": "user", "content": f"Audit this Payload:\n\n{payload[:15000]}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Logic Link Fault.", "severity": "Critical", "remediation": "Check system secrets."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_context = f"You are AEGIS Expert Consultant. Payload: {original_payload[:5000]}. Vulnerabilities: {json.dumps(scan_results)}. Provide expert advice on fixing flaws or optimizing artistic flow."
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
# 4. DASHBOARD (Universal Logic Layout)
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>🛡️ AEGIS</h1><p class='subtitle'>UNIVERSAL LOGIC & EXECUTION GUARANTY</p></div>", unsafe_allow_html=True)

# 3-Column Grid for Expanded Capabilities
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-title">💻 Code Security</div>
        <div class="feature-desc">Source audit for Python, JS & APIs.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🤖 Workflow Logic</div>
        <div class="feature-desc">AI automation & business flow audit.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">🔗 Smart Contracts</div>
        <div class="feature-desc">Solidity & Rust exploit analysis.</div>
    </div>
    <div class="feature-card music-glow">
        <div class="feature-title">🎵 Setlist Logic</div>
        <div class="feature-desc">Energy curve & transition audit for shows.</div>
    </div>
    <div class="feature-card music-glow">
        <div class="feature-title">🎸 Song Structure</div>
        <div class="feature-desc">Analyze chord flow & hit-potential.</div>
    </div>
    <div class="feature-card">
        <div class="feature-title">⚖️ Legal Assets</div>
        <div class="feature-desc">NDA & contract liability scan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("📖 HOW TO USE & EXPERT ADVICE"):
    st.markdown("""
    <div class="guide-box">
        <p style='color: #e3b341; font-weight: 600;'>💡 UNIVERSAL ADVICE:</p>
        <p style='font-size: 13px; color: #8b949e;'>
        <b>For Musicians:</b> Paste your setlist (Song titles + BPM/Key) or your song's chord progression. AEGIS will find logic gaps in your show flow or songwriting structure.
        </p>
    </div>
    """, unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste code, business logic, or your music setlist here...")

if st.button("🚀 INITIATE LOGIC AUDIT"):
    if not payload.strip():
        st.error("❌ ERROR: Payload is empty.")
    else:
        with st.spinner("Analyzing Logic across Neural Clusters..."):
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
        st.subheader("🚨 Logic Matrix")
        f0 = findings[0]
        st.error(f"**[{f0.get('severity')}]:** {f0.get('issue')}\n\n*Fix/Optimization: {f0.get('remediation')}*")
        
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ Enterprise/Music Access Granted:")
                for i in range(1, len(findings)):
                    item = findings[i]
                    with st.expander(f"[{item.get('severity')}] {item.get('issue')}", expanded=True):
                        st.write(f"**Remediation/Advice:** {item.get('remediation')}")
                
                # 💬 UNIVERSAL CONSULTANT
                st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
                st.subheader("💬 AI Consultant (Expert Edition)")
                for m in st.session_state.chat_history:
                    with st.chat_message(m["role"]): st.markdown(m["content"])
                if prompt := st.chat_input("Ask AEGIS about your audit or songwriting..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"): st.markdown(prompt)
                    with st.chat_message("assistant"):
                        reply = chat_with_consultant(prompt, payload, findings)
                        st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='locked-content'>🔒 <b>{len(findings)-1} ADDITIONAL INSIGHTS HIDDEN</b><br>Unlock the Full Matrix to optimize your logic or musical performance.</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b = st.columns([2,1])
                with col_a: u_code = st.text_input("ENTER PREMIUM PASSCODE:", type="password")
                with col_b:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔓 UNLOCK"):
                        if u_code == st.secrets["AEGIS_PASSCODE"]:
                            st.session_state.unlocked = True
                            st.rerun()
                        else: st.error("Invalid Code.")
                st.markdown("[👉 **Get Premium Pass ($9)**](https://porschza.gumroad.com/l/AEGIS)")

st.markdown("<div class='custom-footer'>AEGIS v7.4 | Art of Logic Edition | Secured by Enterprise Trust Layer</div>", unsafe_allow_html=True)
