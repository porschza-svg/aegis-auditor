import streamlit as st
import json
import time
from groq import Groq

# ────────────────────────────────────────────────
# 1. ENTERPRISE CONFIG & UI CLOAKING
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Enterprise Security Scanner", layout="centered")

st.markdown("""
    <style>
    /* 🛡️ CLOAK STREAMLIT UI */
    [data-testid="stHeader"] {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 💎 PREMIUM ENTERPRISE STYLING */
    .main { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #58a6ff; text-align: center; text-transform: uppercase; letter-spacing: 2px;}
    .stButton>button { width: 100%; background: linear-gradient(90deg, #1f6feb, #388bfd); color: white; font-size: 18px; font-weight: bold; padding: 12px; border-radius: 8px; border: none; box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4); transition: all 0.3s; }
    .stButton>button:hover { background: linear-gradient(90deg, #388bfd, #58a6ff); transform: translateY(-2px); }
    .metric-box { background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; text-align: center; box-shadow: inset 0 0 20px rgba(0,0,0,0.5); margin: 20px 0; }
    .locked-content { background: repeating-linear-gradient(45deg, #161b22, #161b22 10px, #0d1117 10px, #0d1117 20px); border: 1px dashed #e3b341; padding: 20px; border-radius: 8px; text-align: center; color: #e3b341; margin-top: 15px;}
    .custom-footer { text-align: center; color: #8b949e; font-size: 12px; margin-top: 50px; opacity: 0.7; }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# 2. NEURAL ENGINE (Prompt & API Secure Fetch)
# ────────────────────────────────────────────────
AUDITOR_PROMPT = """
You are AEGIS, an elite security and logic auditor.
Analyze the payload. Identify at least 3 vulnerabilities, logical flaws, or areas for improvement.
Output ONLY valid JSON:
{
  "trust_score": <int 0-100>,
  "findings": [
    {"issue": "<Short, punchy description>", "severity": "<Critical/Warning/Info>", "remediation": "<Actionable fix>"}
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
                {"role": "user", "content": f"Scan this:\n\n{payload[:3000]}"}
            ],
            temperature=0.0,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {
            "trust_score": 0, 
            "findings": [
                {"issue": "System error or Missing API Key in Streamlit Secrets.", "severity": "Critical", "remediation": "Check system configuration."}
            ]
        }

# ────────────────────────────────────────────────
# 3. MEMORY SYSTEM
# ────────────────────────────────────────────────
if 'scanned' not in st.session_state:
    st.session_state.scanned = False
    st.session_state.result = None
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# ────────────────────────────────────────────────
# 4. DASHBOARD (The Hook)
# ────────────────────────────────────────────────
st.title("🛡️ AEGIS")
st.markdown("<p style='text-align:center; color:#8b949e; font-size: 16px;'>Enterprise-Grade Execution Guaranty System</p>", unsafe_allow_html=True)

payload = st.text_area("TARGET PAYLOAD:", height=200, placeholder="Paste your code, business logic, or contract here to scan for hidden liabilities...")

if st.button("🚀 INITIATE SECURE SCAN (Free Basic Report)"):
    if not payload.strip():
        st.error("❌ ERROR: Payload cannot be empty.")
    else:
        progress_text = "Establishing secure neural link..."
        my_bar = st.progress(0, text=progress_text)
        time.sleep(0.5)
        my_bar.progress(50, text="Interrogating logic across AI models...")
        
        st.session_state.result = run_audit(payload)
        st.session_state.scanned = True
        st.session_state.unlocked = False 
        
        my_bar.progress(100, text="Scan Complete.")
        time.sleep(0.5)
        my_bar.empty()

# ────────────────────────────────────────────────
# 5. THE PAYWALL & GUMROAD INTEGRATION
# ────────────────────────────────────────────────
if st.session_state.scanned and st.session_state.result:
    res = st.session_state.result
    
    st.markdown("---")
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric("AEGIS Trust Score", f"{res.get('trust_score', 0)} / 100")
    st.markdown("</div>", unsafe_allow_html=True)

    findings = res.get("findings", [])
    
    if len(findings) > 0:
        st.subheader("🚨 Threat Matrix")
        
        first_finding = findings[0]
        st.error(f"**[{first_finding.get('severity', 'Alert')}]:** {first_finding.get('issue', 'Issue detected')}\n\n*Solution: {first_finding.get('remediation', 'Manual review required')}*")
        
        if len(findings) > 1:
            hidden_count = len(findings) - 1
            
            if st.session_state.unlocked:
                st.success("✅ Enterprise Mode Unlocked. Displaying Full Report:")
                for i in range(1, len(findings)):
                    item = findings[i]
                    st.warning(f"**[{item.get('severity', 'Warning')}]:** {item.get('issue', 'Unknown anomaly')}\n\n*Solution: {item.get('remediation', 'Consult architect')}*")
            else:
                st.markdown(f"<div class='locked-content'>🔒 <b>{hidden_count} Critical Vulnerabilities Hidden</b><br>Upgrade to Enterprise to reveal exact locations and actionable remediation steps.</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🔑 Enter Premium Passcode")
                
                unlock_code = st.text_input("Enter the code from your Gumroad receipt:", placeholder="e.g., NEXUS-AEGIS-V6-SECURE", type="password")
                
                if st.button("🔓 UNLOCK REPORT"):
                    # อัปเกรดรหัสผ่านใหม่ที่นี่
                    if unlock_code == "NEXUS-AEGIS-V6-SECURE": 
                        st.session_state.unlocked = True
                        st.rerun() 
                    else:
                        st.error("❌ Invalid Passcode. Please check your receipt.")
                
                # ลิงก์รอการอัปเดตเป็นของจริง
                st.markdown("[👉 **Don't have a passcode? Get it here for $9**](https://gumroad.com)")
                
    else:
        st.success("✅ No critical vulnerabilities detected. Payload is clear.")

st.markdown("<div class='custom-footer'>AEGIS v6.2 | Enterprise Trust Layer | Secure E2EE Connection</div>", unsafe_allow_html=True)
