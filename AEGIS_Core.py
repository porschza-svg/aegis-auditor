import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. SOVEREIGN UI CONFIG & ANIMATION
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Global Authority Auditor", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    /* 🛡️ SYSTEM CLOAKING */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', sans-serif; }
    
    /* 💎 GLOBAL HERO SECTION */
    .hero-container { text-align: center; padding: 40px 0 30px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 10px; font-weight: 900; margin-bottom: 5px; text-shadow: 0 0 40px rgba(88, 166, 255, 0.6); font-size: 3.5rem; }
    .subtitle { color: #8b949e; font-size: 14px; letter-spacing: 4px; margin-bottom: 45px; text-transform: uppercase; opacity: 0.9; }

    /* ⚡ HIGH-CONVERSION MATRIX GRID (3x2) */
    div[data-testid="stExpander"] { background: rgba(22, 27, 34, 0.5); border: 1px solid #30363d !important; border-radius: 16px !important; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    div[data-testid="stExpander"]:hover { border-color: #58a6ff !important; transform: translateY(-5px); box-shadow: 0 10px 40px rgba(31, 111, 235, 0.2); }
    .expander-title { color: #58a6ff; font-weight: 800; font-size: 12px; letter-spacing: 1px; }

    /* 📘 AUTHORITY MANUAL */
    .guide-box { background: linear-gradient(145deg, #161b22 0%, #0d1117 100%); border-radius: 16px; padding: 30px; border: 1px solid #30363d; margin-bottom: 40px; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); }
    .status-badge { background: #238636; color: white; padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 800; letter-spacing: 1px; margin-bottom: 20px; display: inline-block; }

    /* 📥 TARGET PAYLOAD */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 16px !important; color: #e6edf3 !important; padding: 25px !important; font-family: 'Fira Code', monospace; font-size: 15px; transition: 0.3s; }
    .stTextArea textarea:focus { border-color: #58a6ff !important; box-shadow: 0 0 0 4px rgba(88, 166, 255, 0.1) !important; }
    
    /* 🚀 FINAL CALL-TO-ACTION */
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 20px; font-weight: 900; padding: 20px; border-radius: 16px; border: none; box-shadow: 0 15px 45px rgba(31, 111, 235, 0.4); letter-spacing: 3px; transition: 0.5s; text-transform: uppercase; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 20px 60px rgba(31, 111, 235, 0.7); }

    /* 📊 REVENUE GATEWAY */
    .score-display { background: #0d1117; padding: 50px; border-radius: 30px; border: 1px solid #30363d; text-align: center; margin: 50px 0; border-top: 4px solid #58a6ff; }
    .locked-card { background: rgba(227, 179, 65, 0.05); border: 2px dashed #e3b341; padding: 40px; border-radius: 20px; text-align: center; color: #e3b341; margin-top: 30px; }
    
    .custom-footer { text-align: center; color: #484f58; font-size: 12px; margin-top: 120px; padding-bottom: 50px; border-top: 1px solid #21262d; padding-top: 40px; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. UNIVERSAL AUDITOR CORE (v9.0)
# ────────────────────────────────────────────────
def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS, the Supreme Universal Auditor. Detect 3 high-impact logic flaws in Code, Business, or Music. Provide professional, actionable remediation. Output JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"},
                {"role": "user", "content": payload[:15000]}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Secure Link Fault.", "severity": "Critical", "remediation": "Audit interrupted. Check system integrity."}]}

def chat_consultant(user_input, payload, results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        sys_msg = f"You are AEGIS Global Consultant. Deep-dive into this payload: {payload[:5000]}. Vulnerabilities: {json.dumps(results)}. Solve for the user."
        msgs = [{"role": "system", "content": sys_msg}]
        for m in st.session_state.chat_history: msgs.append(m)
        msgs.append({"role": "user", "content": user_input})
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=0.5)
        return resp.choices[0].message.content
    except: return "⚠️ Sync Error."

# ────────────────────────────────────────────────
# 3. GLOBAL MEMORY
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ────────────────────────────────────────────────
# 4. FINAL SOVEREIGN DASHBOARD
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>🛡️ AEGIS</h1><p class='subtitle'>THE UNIVERSAL LOGIC AUTHORITY</p></div>", unsafe_allow_html=True)

# ⚡ THE DEEP INTELLIGENCE MATRIX (Final Polish)
st.markdown("<div class='status-badge'>● NEURAL LINK: ACTIVE</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    with st.expander("💻 CODE SECURITY"):
        st.caption("Deep-Intelligence Audit for Python, JS & APIs. Detect logic bombs & leaks.")
    with st.expander("🎵 SETLIST LOGIC"):
        st.caption("Emotional Arc Engineering. Optimize energy curve for live performance.")
with c2:
    with st.expander("🤖 WORKFLOW LOGIC"):
        st.caption("B2B Agent Integrity Audit. Solve logic loops & workflow deadlocks.")
    with st.expander("🎸 SONG STRUCTURE"):
        st.caption("Hit Potential Analysis. Breakdown hook density & songwriting logic.")
with c3:
    with st.expander("🔗 SMART CONTRACTS"):
        st.caption("Web3 Exploit Shield. Audit Reentrancy & Logic flaws in Solidity/Rust.")
    with st.expander("⚖️ LEGAL ASSETS"):
        st.caption("Liability Loop Detection. Scan NDAs & contracts for hidden legal risks.")

# 📘 FINAL OPERATIONAL MANUAL
with st.expander("📖 READ BEFORE EXECUTION: OPERATIONAL MANUAL"):
    st.markdown("<div class='guide-box'>", unsafe_allow_html=True)
    st.write("**AEGIS** is a deep-intelligence auditor that interrogates the 'Intent' behind your assets, not just the syntax. Whether you are a Developer securing code or a Musician optimizing a show, AEGIS reveals hidden logic flaws.")
    tab_a, tab_b = st.tabs(["🚀 Tech & Business", "🎸 Music & Arts"])
    with tab_a:
        st.write("1. **Paste Source/Logic** in the Target Payload box.\n2. **Execute Audit** to reveal your global Trust Score.\n3. **Unlock Premium** for full remediation & AI Consultant access.")
    with tab_b:
        st.write("1. **Paste Setlist/Chords** (e.g. Song Title + Key/BPM).\n2. **Execute Audit** to analyze energy curve & transitions.\n3. **Chat with AI** to optimize your performance logic.")
    st.markdown("</div>", unsafe_allow_html=True)

# 📥 FINAL TARGET INPUT
payload = st.text_area("TARGET PAYLOAD:", height=300, placeholder="Enter enterprise assets or musical structures for deep-intelligence audit...")

if st.button("🚀 INITIATE GLOBAL SCAN"):
    if not payload.strip(): st.error("❌ ERROR: Payload required.")
    else:
        with st.spinner("Executing Logic Audit across Neural Clusters..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False 
            st.session_state.chat_history = []
            st.rerun()

# ────────────────────────────────────────────────
# 5. RESULTS & REVENUE (High-Conversion Edition)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown(f"<div class='score-display'><h3>GLOBAL TRUST SCORE</h3><h1 style='font-size: 100px; color:#58a6ff; margin:0;'>{res.get('trust_score', 0)}%</h1><p style='color:#8b949e;'>Based on Universal Logic Standards</p></div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Logic Matrix Analysis")
        st.error(f"**[{findings[0].get('severity')}]:** {findings[0].get('issue')}\n\n*Immediate Fix: {findings[0].get('remediation')}*")
        
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ SOVEREIGN ACCESS GRANTED")
                for i in range(1, len(findings)):
                    with st.expander(f"[{findings[i].get('severity')}] {findings[i].get('issue')}", expanded=True):
                        st.write(f"**Remediation:** {findings[i].get('remediation')}")
                # AI Consultant Module...
                st.markdown("<div style='background:#0d1117; padding:30px; border-radius:20px; border:1px solid #30363d; margin-top:40px;'>", unsafe_allow_html=True)
                st.subheader("💬 AI Expert Consultant")
                for m in st.session_state.chat_history:
                    with st.chat_message(m["role"]): st.markdown(m["content"])
                if prompt := st.chat_input("Request deeper analysis..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    reply = chat_consultant(prompt, payload, findings)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='locked-card'>🔒 <b>{len(findings)-1} ADDITIONAL LOGIC GAPS DETECTED</b><br>Upgrade to reveal the full audit matrix and unlock the Expert Consultant module.</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                col_x, col_y = st.columns([3,1])
                with col_x: u_code = st.text_input("PREMIUM PASSCODE:", type="password", placeholder="Enter your Enterprise Key...")
                with col_y:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔓 UNLOCK"):
                        if u_code == st.secrets["AEGIS_PASSCODE"]:
                            st.session_state.unlocked = True
                            st.rerun()
                        else: st.error("Access Denied.")
                st.markdown(f"<div style='text-align:center; margin-top:15px;'><a href='https://porschza.gumroad.com/l/AEGIS' target='_blank' style='color:#e3b341; text-decoration:none; font-weight:800;'>👉 SECURE YOUR ENTERPRISE PASS INSTANTLY ($9)</a></div>", unsafe_allow_html=True)

st.markdown("<div class='custom-footer'>AEGIS v9.0 | Global Authority Edition | Final Market Entry Ready</div>", unsafe_allow_html=True)
