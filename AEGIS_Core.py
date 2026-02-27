import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ARCHITECTURAL UI CONFIG (Obsidian Theme)
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Obsidian Sovereignty", layout="centered", page_icon="🛡️")

st.markdown("""
    <style>
    /* 🛡️ CLOAK & CLEANUP */
    [data-testid="stHeader"], #MainMenu, footer {visibility: hidden;}
    .main { background-color: #0b0e14; color: #f0f6fc; font-family: 'Inter', -apple-system, sans-serif; }
    
    /* 💎 CINEMATIC HEADER */
    .hero-container { text-align: center; padding: 40px 0 20px 0; }
    h1 { color: #ffffff; text-transform: uppercase; letter-spacing: 8px; font-weight: 900; margin-bottom: 0px; text-shadow: 0 0 30px rgba(88, 166, 255, 0.5); font-size: 3rem; }
    .subtitle { color: #8b949e; font-size: 13px; letter-spacing: 3px; margin-bottom: 40px; text-transform: uppercase; opacity: 0.8; }

    /* ⚡ UNIFIED INTELLIGENCE MATRIX (3x2 Grid) */
    .matrix-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 30px; }
    div[data-testid="stExpander"] { background: rgba(22, 27, 34, 0.4); border: 1px solid #30363d !important; border-radius: 12px !important; transition: 0.3s; }
    div[data-testid="stExpander"]:hover { border-color: #58a6ff !important; background: rgba(31, 111, 235, 0.05); }

    /* 📘 MANUAL STYLING */
    .guide-section { background: #161b22; border-radius: 12px; padding: 25px; border: 1px solid #30363d; margin-bottom: 30px; }
    .guide-tab-content { padding-top: 15px; font-size: 14px; line-height: 1.6; }

    /* 📥 TARGET PAYLOAD CONTAINER */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid #30363d !important; border-radius: 12px !important; color: #e6edf3 !important; padding: 20px !important; font-family: 'Fira Code', monospace; transition: 0.3s; }
    .stTextArea textarea:focus { border-color: #58a6ff !important; box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2) !important; }
    
    /* 🚀 ACTION BUTTON (SUPER-CHARGED) */
    .stButton>button { width: 100%; background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); color: white; font-size: 18px; font-weight: 800; padding: 18px; border-radius: 12px; border: none; box-shadow: 0 10px 30px rgba(31, 111, 235, 0.4); letter-spacing: 2px; transition: 0.4s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 15px 40px rgba(31, 111, 235, 0.6); }

    /* 📊 SCORE & RESULTS */
    .score-box { background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); padding: 40px; border-radius: 24px; border: 1px solid #30363d; text-align: center; margin: 40px 0; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    .custom-footer { text-align: center; color: #484f58; font-size: 11px; margin-top: 100px; padding-bottom: 40px; border-top: 1px solid #21262d; padding-top: 30px; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL AUDITOR ENGINE (v8.1)
# ────────────────────────────────────────────────
def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are AEGIS, the Global Sovereignty Auditor. Detect 3 critical logic flaws. For music, analyze energy/flow. Output JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"},
                {"role": "user", "content": payload[:15000]}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except: return {"trust_score": 0, "findings": [{"issue": "Link Interrupted.", "severity": "Critical", "remediation": "Sync failure."}]}

def chat_with_consultant(user_input, original_payload, scan_results):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        sys_msg = f"You are AEGIS Global Consultant. Payload Context: {original_payload[:5000]}. Vulnerabilities: {json.dumps(scan_results)}."
        msgs = [{"role": "system", "content": sys_msg}]
        for m in st.session_state.chat_history: msgs.append(m)
        msgs.append({"role": "user", "content": user_input})
        resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs, temperature=0.5)
        return resp.choices[0].message.content
    except: return "⚠️ Interrupted."

# ────────────────────────────────────────────────
# 3. GLOBAL MEMORY
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state: st.session_state.scanned = False
if 'result' not in st.session_state: st.session_state.result = None
if 'unlocked' not in st.session_state: st.session_state.unlocked = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# ────────────────────────────────────────────────
# 4. OBSIDIAN DASHBOARD (Final Polish)
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>🛡️ AEGIS</h1><p class='subtitle'>OBSIDIAN SOVEREIGNTY | UNIVERSAL LOGIC AUDITOR</p></div>", unsafe_allow_html=True)

# ⚡ THE INTELLIGENCE MATRIX (Unified Expander Grid)
st.markdown("<p style='font-size: 11px; color: #58a6ff; font-weight: 800; margin-bottom: 10px;'>DEEP INTELLIGENCE MODULES:</p>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    with st.expander("💻 CODE SECURITY"):
        st.caption("Logic Bombs & API Audit. Detect hidden leaks in source code.")
    with st.expander("🎵 SETLIST LOGIC"):
        st.caption("Emotional Arc Engineering. Optimize show energy curve.")
with c2:
    with st.expander("🤖 WORKFLOW LOGIC"):
        st.caption("Agent Integrity. Identify deadlocks in AI automation.")
    with st.expander("🎸 SONG STRUCTURE"):
        st.caption("Hit Density Theory. Analyze hook flow & patterns.")
with c3:
    with st.expander("🔗 SMART CONTRACTS"):
        st.caption("Exploit Analysis. Audit Reentrancy in Solidity/Rust.")
    with st.expander("⚖️ LEGAL ASSETS"):
        st.caption("Liability Loop Detection. Scan NDAs for hidden risks.")

# 📖 ENHANCED MANUAL
with st.expander("📖 OPERATIONAL MANUAL & ARCHITECT'S ADVICE"):
    st.markdown("<div class='guide-section'>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🚀 Tech / Business", "🎸 Music / Art"])
    with t1:
        st.markdown("<div class='guide-tab-content'><b>1. Input:</b> Paste code or logic in the Payload box.<br><b>2. Scan:</b> Receive your 0-100% Trust Score.<br><b>3. Unlock:</b> Get full remediation steps ($9).</div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div class='guide-tab-content'><b>1. Input:</b> List Songs + Key/BPM or Chord flow.<br><b>2. Scan:</b> Analyze energy curve & transitions.<br><b>3. Expert:</b> Chat with Consultant to fix show gaps.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 📥 INPUT AREA
payload = st.text_area("TARGET PAYLOAD:", height=280, placeholder="Paste your enterprise or musical assets here for deep-intelligence audit...")

if st.button("🚀 INITIATE GLOBAL LOGIC AUDIT"):
    if not payload.strip(): st.error("❌ ERROR: Payload required.")
    else:
        with st.spinner("Executing Logic Audit across Neural Clusters..."):
            st.session_state.result = run_audit(payload)
            st.session_state.scanned = True
            st.session_state.unlocked = False 
            st.session_state.chat_history = []
            st.rerun()

# ────────────────────────────────────────────────
# 5. RESULTS & REVENUE (No Functionality Removed)
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown(f"<div class='score-box'><h3>GLOBAL TRUST SCORE</h3><h1 style='font-size: 85px; color:#58a6ff; margin:0;'>{res.get('trust_score', 0)}%</h1></div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Logic Matrix Summary")
        st.error(f"**[{findings[0].get('severity')}]:** {findings[0].get('issue')}\n\n*Solution: {findings[0].get('remediation')}*")
        
        if len(findings) > 1:
            if st.session_state.unlocked:
                st.success("✅ SOVEREIGN ACCESS GRANTED")
                for i in range(1, len(findings)):
                    with st.expander(f"[{findings[i].get('severity')}] {findings[i].get('issue')}", expanded=True):
                        st.write(findings[i].get('remediation'))
                
                # Chat with Consultant
                st.markdown("<div style='background:#0d1117; padding:20px; border-radius:15px; border:1px solid #30363d;'>", unsafe_allow_html=True)
                st.subheader("💬 AI Expert Consultant")
                for m in st.session_state.chat_history:
                    with st.chat_message(m["role"]): st.markdown(m["content"])
                if prompt := st.chat_input("Ask for deeper analysis..."):
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    reply = chat_with_consultant(prompt, payload, findings)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:rgba(227,179,65,0.05); border:1px dashed #e3b341; padding:30px; border-radius:15px; text-align:center; color:#e3b341;'>🔒 <b>{len(findings)-1} ADDITIONAL LOGIC GAPS DETECTED</b><br>Unlock the Full Sovereignty Matrix & AI Consultant.</div>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b = st.columns([3,1])
                with col_a: u_code = st.text_input("ENTER PREMIUM PASSCODE:", type="password")
                with col_b: 
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔓 UNLOCK"):
                        if u_code == st.secrets["AEGIS_PASSCODE"]:
                            st.session_state.unlocked = True
                            st.rerun()
                st.markdown("[👉 **Instant Premium Access ($9)**](https://porschza.gumroad.com/l/AEGIS)")

st.markdown("<div class='custom-footer'>AEGIS v8.1 | Obsidian Sovereignty | Secured by Enterprise Trust Layer</div>", unsafe_allow_html=True)
