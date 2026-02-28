import streamlit as st
import json
import time
import io
from groq import Groq

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
    .locked-card { background: rgba(227, 179, 65, 0.08); border: 1px dashed #e3b341; padding: 30px; border-radius: 16px; text-align: center; color: #e3b341; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. AUDIT ENGINE (ROBUST VERSION)
# ────────────────────────────────────────────────
def run_aegis_audit(payload, audio_meta=None):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        audio_context = f" [AUDIO_UPLINK_METADATA: {audio_meta}]" if audio_meta else ""
        
        system_prompt = (
            "You are AEGIS, the Supreme Universal Auditor by WAT SYSTEMS. "
            "Detect 3 critical logic flaws. For Code/Business: Focus on structural integrity. "
            "For Music: Analyze structural integrity (Intro/Verse/Chorus balance) and emotional arc logic. "
            "Output JSON ONLY: {\"trust_score\": int, \"findings\": [{\"issue\": str, \"severity\": str, \"remediation\": str}]}"
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"PAYLOAD: {payload[:12000]}{audio_context}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        # Clean JSON in case of formatting artifacts
        raw_content = response.choices[0].message.content.strip()
        return json.loads(raw_content)
    except Exception as e: 
        return {"trust_score": 0, "findings": [{"issue": "Uplink Error.", "severity": "Critical", "remediation": f"Verify System Key. (Internal: {str(e)})"}]}

# ────────────────────────────────────────────────
# 3. DASHBOARD ARCHITECTURE
# ────────────────────────────────────────────────
st.markdown("<div class='hero-container'><h1>AEGIS</h1><div class='brand-tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div></div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#238636; font-size:10px; font-weight:800; letter-spacing:2px; margin-bottom:20px;'>● NEURAL LINK: ACTIVE</div>", unsafe_allow_html=True)

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
st.markdown("<div class='uplink-box'>", unsafe_allow_html=True)
st.markdown("<span style='color:#388bfd; font-size:12px; font-weight:800; letter-spacing:2px;'>🛰️ SOVEREIGN AUDIO UPLINK</span>", unsafe_allow_html=True)
audio_file = st.file_uploader("Upload musical payload", type=['mp3', 'wav'], label_visibility="collapsed")
if audio_file:
    st.success(f"Uplink Established: {audio_file.name}")
st.markdown("</div>", unsafe_allow_html=True)

# 📥 PAYLOAD INPUT
payload = st.text_area("TARGET PAYLOAD:", height=250, placeholder="Paste assets or musical logic for deep-intelligence audit...")

if st.button("🚀 INITIATE GLOBAL SCAN"):
    if not payload.strip() and not audio_file:
        st.error("❌ ERROR: No payload detected.")
    else:
        with st.spinner("Extracting structural truth..."):
            audio_info = f"File: {audio_file.name}, Size: {audio_file.size} bytes" if audio_file else None
            st.session_state.result = run_aegis_audit(payload, audio_info)
            st.session_state.scanned = True
            st.session_state.unlocked = False
            st.rerun()

# ────────────────────────────────────────────────
# 4. RESULTS
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    st.markdown("---")
    st.markdown(f"<div class='score-display'><h3>GLOBAL TRUST SCORE</h3><h1 style='font-size: 80px; color:#58a6ff; margin:0;'>{res.get('trust_score', 0)}%</h1><p style='color:#8b949e;'>Universal Logic Standard</p></div>", unsafe_allow_html=True)
    
    findings = res.get("findings", [])
    if findings:
        st.subheader("🚨 Logic Matrix Analysis")
        st.error(f"**[{findings[0].get('severity')}]:** {findings[0].get('issue')}\n\n*Fix: {findings[0].get('remediation')}*")
        
        if not st.session_state.unlocked:
            st.markdown(f"<div class='locked-card'>🔒 <b>{len(findings)-1} ADDITIONAL LOGIC GAPS DETECTED</b><br>Upgrade for full Matrix access.</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center; margin-top:15px;'><a href='[https://porschza.gumroad.com/l/AEGIS](https://porschza.gumroad.com/l/AEGIS)' target='_blank' style='color:#e3b341; text-decoration:none; font-weight:800;'>👉 SECURE ENTERPRISE PASS ($9)</a></div>", unsafe_allow_html=True)
            
            passcode = st.text_input("ENTER PASSCODE:", type="password")
            if st.button("🔓 VERIFY"):
                if passcode == st.secrets.get("AEGIS_PASSCODE", "1234"):
                    st.session_state.unlocked = True
                    st.rerun()
                else: st.error("Access Denied.")
        else:
            st.success("✅ SOVEREIGN ACCESS GRANTED")
            for i in range(1, len(findings)):
                with st.expander(f"[{findings[i].get('severity')}] {findings[i].get('issue')}", expanded=True):
                    st.write(findings[i].get('remediation'))
    
    if st.button("🔄 CLEAR SCAN"):
        st.session_state.scanned = False
        st.session_state.result = None
        st.rerun()

st.markdown("<div style='text-align:center; color:#484f58; font-size:10px; margin-top:100px; letter-spacing:2px;'>POWERED BY WAT SYSTEMS | AEGIS v10.0</div>", unsafe_allow_html=True)
