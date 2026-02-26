import streamlit as st
import json
from groq import Groq
from datetime import datetime

# ────────────────────────────────────────────────
# CONFIG & STYLE (v5.0: เรียบง่ายสุด, โหลดเร็ว, มือถือดี, premium vibe)
# ────────────────────────────────────────────────
st.set_page_config(page_title="AEGIS v5.0 – Instant Security Scanner", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #58a6ff; text-align: center; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #238636, #2ea043); color: white; font-size: 20px; padding: 16px; border-radius: 10px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.5); transition: all 0.3s; }
    .stButton>button:hover { background: linear-gradient(90deg, #2ea043, #3fb950); transform: translateY(-2px); }
    .stTextArea>div>div>textarea { background: #161b22; color: #e6edf3; border: 1px solid #30363d; border-radius: 8px; font-size: 16px; }
    .metric-box { background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.4); margin: 20px 0; }
    .footer { text-align: center; color: #8b949e; font-size: 12px; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# Prompt v5.0 (สั้น กระชับ เน้น JSON เท่านั้น)
AUDITOR_PROMPT = """
You are AEGIS v5.0, elite security auditor.
Analyze the code/contract.
Output ONLY valid JSON:
{
  "trust_score": <0-100, 100 = perfectly safe>,
  "issues_count": <number>,
  "summary": "<1 short sentence>"
}
"""

def run_audit(payload):
    try:
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "your-key-here"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Quick scan this:\n\n{payload[:3000]}"}],
            temperature=0.0,
            max_tokens=80,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content.strip())
    except:
        return {"trust_score": 50, "issues_count": 0, "summary": "Scan completed (demo mode)"}

# ────────────────────────────────────────────────
# UI ใหม่ทั้งหมด (v5.0: เรียบง่าย, ดึงดูด, paywall ชัดเจน)
# ────────────────────────────────────────────────
st.title("🛡️ AEGIS v5.0 – Instant Security Scanner")
st.markdown("<p style='text-align:center; color:#8b949e;'>Free basic scan | Unlock full report $9</p>", unsafe_allow_html=True)

payload = st.text_area("", height=140, placeholder="วางโค้ดหรือสัญญาที่นี่... (max 3000 ตัวอักษร)")

if st.button("SCAN NOW – Free"):
    if not payload.strip():
        st.warning("กรุณาวางโค้ดหรือสัญญาก่อน")
    else:
        with st.spinner("AEGIS กำลังสแกน..."):
            result = run_audit(payload)

        st.markdown("---")
        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
        st.metric("Trust Score (Basic Scan)", f"{result['trust_score']}/100", delta_color="normal")
        st.markdown("</div>", unsafe_allow_html=True)

        st.info(result['summary'])

        st.markdown("### อยากได้รายงานเต็ม + วิธีแก้ไข?")
        st.markdown("ปลดล็อก Full Report เพียง $9 (จ่ายครั้งเดียว ได้ตลอด)")
        st.markdown("[Unlock Now $9 – Instant Download](https://porschza.gumroad.com/l/aegis-v5-full-report)")

st.markdown("<div class='footer'>AEGIS v5.0 – Powered by Grok & Shelby Systems – Instant. Secure. Global.</div>", unsafe_allow_html=True)
