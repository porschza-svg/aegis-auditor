import streamlit as st
import pandas as pd
import json
from groq import Groq

# ────────────────────────────────────────────────
# 1. System Config & Prompts
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS | Enterprise Trust Layer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stButton>button { width: 100%; border-radius: 6px; background-color: #1f6feb; color: white; border: none; font-weight: bold; padding: 10px; transition: 0.3s; }
    .stButton>button:hover { background-color: #388bfd; border-color: #8b949e; }
    .metric-container { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

AUDITOR_PROMPT = """
You are AEGIS, an elite AI Security Auditor.
Analyze the provided payload (source code or legal contract).
Identify vulnerabilities, logic flaws, or risks.
You MUST output ONLY valid JSON.
Structure:
{
  "risk_score": <int 0-100, 100 is perfectly safe>,
  "findings": [
    {
      "severity": "<Critical/Warning/Info>",
      "issue": "<Clear description>",
      "recommendation": "<Direct, actionable fix>"
    }
  ]
}
"""

def run_aegis_audit(api_key, payload, model_name):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": AUDITOR_PROMPT},
                {"role": "user", "content": f"PAYLOAD TO ANALYZE:\n\n{payload}"}
            ],
            temperature=0.0,
            max_tokens=1024,
            response_format={"type": "json_object"} 
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception as e:
        return {"risk_score": 0, "findings": [{"severity": "Error", "issue": "System Failure", "recommendation": "Check API limits or network."}]}

# ────────────────────────────────────────────────
# 2. Memory Initialization (แก้ปัญหาผลลัพธ์หาย)
# ────────────────────────────────────────────────
if 'audit_complete' not in st.session_state:
    st.session_state.audit_complete = False
    st.session_state.final_score = 0
    st.session_state.score_1 = 0
    st.session_state.score_2 = 0
    st.session_state.all_findings = []

# ────────────────────────────────────────────────
# 3. Command Center UI
# ────────────────────────────────────────────────
st.title("🛡️ AEGIS: Enterprise Execution Guaranty System")
st.caption("v2.0 | Cross-Model Interrogation Protocol | Authorized Personnel Only")
st.markdown("---")

groq_key = st.text_input("🔑 INITIALIZE SYSTEM: Enter GROQ API KEY", type="password")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Target Payload")
    payload_input = st.text_area("Inject Code or Contract here:", height=300, 
                                 placeholder="Paste defective code, COBOL logic, or a shady NDA contract...")

with col2:
    st.subheader("Interrogation Matrix")
    st.write("Active Auditing Models:")
    st.success("🧠 Primary: Llama 3.3 70B (Deep Logic & Context)")
    st.info("⚡ Redundancy: Llama 3.1 8B (High-Speed Crosscheck)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    start_audit = st.button("🚀 EXECUTE MULTI-MODEL AUDIT")

# ────────────────────────────────────────────────
# 4. Processing Engine 
# ────────────────────────────────────────────────
if start_audit:
    if not groq_key or not payload_input.strip():
        st.error("❌ ERROR: Valid GROQ API KEY and Payload are required.")
    else:
        with st.spinner("AEGIS is actively interrogating the payload across neural networks..."):
            result_primary = run_aegis_audit(groq_key, payload_input, "llama-3.3-70b-versatile")
            result_secondary = run_aegis_audit(groq_key, payload_input, "llama-3.1-8b-instant")
            
            score_1 = int(result_primary.get("risk_score", result_primary.get("Risk_Score", 0)))
            score_2 = int(result_secondary.get("risk_score", result_secondary.get("Risk_Score", 0)))
            
            # บันทึกข้อมูลลงสมองของระบบ (Session State)
            st.session_state.score_1 = score_1
            st.session_state.score_2 = score_2
            st.session_state.final_score = (score_1 + score_2) / 2
            
            findings_temp = []
            for res in [result_primary, result_secondary]:
                findings = res.get("findings", res.get("Findings", []))
                if isinstance(findings, list):
                    for item in findings:
                        findings_temp.append({
                            "Severity": str(item.get("severity", "Info")).capitalize(),
                            "Issue": str(item.get("issue", "Unknown anomaly detected.")),
                            "Recommendation": str(item.get("recommendation", "Manual review required."))
                        })
            
            st.session_state.all_findings = findings_temp
            st.session_state.audit_complete = True # บอกระบบว่าตรวจเสร็จแล้วนะ!

# ────────────────────────────────────────────────
# 5. Display Results & Paywall (The Curiosity Gap)
# ────────────────────────────────────────────────
# ใช้เงื่อนไข audit_complete แทน start_audit เพื่อกันจอหายตอนกรอกรหัส
if st.session_state.audit_complete:
    st.markdown("---")
    st.subheader("📊 AEGIS Security Clearance Report")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("AEGIS Final Trust Score", f"{st.session_state.final_score:.1f} / 100")
    with m2:
        st.metric("Llama-3.3-70B Confidence", f"{st.session_state.score_1}")
    with m3:
        st.metric("Llama-3.1-8B Confidence", f"{st.session_state.score_2}")
        
    if st.session_state.all_findings:
        st.markdown("---")
        st.warning(f"🚨 **Analysis Complete:** AEGIS detected **{len(st.session_state.all_findings)} vulnerabilities/issues** in your payload.")
        
        st.markdown("### 🔒 Unlock Detailed Vulnerability Report")
        st.write("To view the exact locations of these vulnerabilities and get actionable remediation steps, please enter your Premium Passcode.")
        
        # ช่องกรอกรหัส คราวนี้พิมพ์แล้วจะไม่เด้งหายแล้ว!
        unlock_code = st.text_input("Enter your Passcode:", type="password", placeholder="e.g. UNLOCK9")
        
        if unlock_code == "UNLOCK9":
            st.success("✅ Access Granted. Displaying Full Enterprise Matrix.")
            df = pd.DataFrame(st.session_state.all_findings)
            
            def color_severity(val):
                if val == 'Critical': return 'color: #ff4b4b; font-weight: bold;'
                elif val == 'Warning': return 'color: #ffa421;'
                return 'color: #3dd56d;'
                
            styled_df = df.style.map(color_severity, subset=['Severity'])
            st.dataframe(styled_df, use_container_width=True)
        elif unlock_code:
            st.error("❌ Invalid Passcode. Please check your purchase receipt.")
        else:
            st.info("👉 **[Get your Premium Passcode for $9 on Gumroad](https://gumroad.com)**")
    else:
        st.success("✅ VERDICT: Payload meets AEGIS enterprise security standards. No vulnerabilities detected.")
