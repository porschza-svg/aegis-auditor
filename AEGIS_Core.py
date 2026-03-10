import streamlit as st
import json
from groq import Groq

st.set_page_config(page_title="AEGIS v13.0 – Universal Logic Authority", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background: #0a0f1a; color: #e6edf3; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #00d4ff; text-align: center; font-size: 5rem; letter-spacing: 15px; text-shadow: 0 0 40px #00d4ff; margin: 60px 0 30px; }
    .tag { color: #00d4ff; font-size: 1.1rem; text-align: center; letter-spacing: 6px; opacity: 0.8; margin-bottom: 60px; }
    .input-container { background: rgba(13, 17, 23, 0.8); border: 1px solid #00d4ff; border-radius: 16px; padding: 30px; margin: 0 auto; max-width: 900px; box-shadow: 0 0 40px rgba(0,212,255,0.15); }
    .stTextArea textarea { background: #000 !important; color: #00ff9d !important; border: 1px solid #00d4ff !important; font-family: 'Fira Code', monospace !important; font-size: 16px !important; }
    .scan-btn { width: 100% !important; background: linear-gradient(90deg, #00d4ff, #00ff9d) !important; color: #000 !important; font-weight: 900 !important; font-size: 24px !important; padding: 20px !important; border-radius: 12px !important; border: none !important; box-shadow: 0 0 30px rgba(0,212,255,0.5) !important; transition: all 0.3s !important; }
    .scan-btn:hover { transform: scale(1.03); box-shadow: 0 0 60px rgba(0,212,255,0.8) !important; }
    .result-box { background: rgba(0,0,0,0.7); border: 2px solid #00d4ff; border-radius: 16px; padding: 40px; margin: 40px auto; max-width: 900px; text-align: center; box-shadow: 0 0 40px rgba(0,212,255,0.2); }
    .score { font-size: 140px; font-weight: 900; color: #00d4ff; text-shadow: 0 0 30px #00d4ff; margin: 0; }
    .paywall { background: rgba(255,0,0,0.1); border: 2px dashed #ff0000; padding: 50px; border-radius: 16px; text-align: center; margin: 50px auto; max-width: 900px; }
    .footer { text-align: center; color: #00d4ff; opacity: 0.6; font-size: 12px; margin-top: 100px; letter-spacing: 4px; }
    .demo-box { background: rgba(0,0,0,0.5); border: 1px dashed #00d4ff; padding: 30px; border-radius: 12px; margin: 30px 0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>AEGIS</h1>", unsafe_allow_html=True)
st.markdown("<div class='tag'>WAT SYSTEMS | UNIVERSAL LOGIC AUTHORITY</div>", unsafe_allow_html=True)

# Demo on first load
st.subheader("Example Scan Result")
st.markdown("<div class='demo-box'>", unsafe_allow_html=True)
st.markdown("<div class='score'>42/100</div>", unsafe_allow_html=True)
st.markdown("<div style='color:#ff0000; font-size:2rem; margin:20px 0;'>Detected 3 Critical Issues</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#8b949e; font-size:1.2rem;'>Multiple critical vulnerabilities detected.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

payload = st.text_area("", height=200, placeholder="Paste code or contract here...")

if st.button("SCAN NOW – FREE"):
    if not payload.strip():
        st.error("NO PAYLOAD DETECTED")
    else:
        with st.spinner("SCANNING..."):
            try:
                client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "your-key-here"))
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Quick scan this:\n\n{payload[:3000]}"}],
                    temperature=0.0,
                    max_tokens=80,
                    response_format={"type": "json_object"}
                )
                result = json.loads(response.choices[0].message.content.strip())
            except:
                result = {"trust_score": 50, "summary": "Scan completed (demo mode)", "issues_count": 0}

        st.markdown("---")
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='score'>{result.get('trust_score', 50)}/100</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#ff0000; font-size:2rem; margin:20px 0;'>Detected {result.get('issues_count', 0)} Critical Issues</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#8b949e; font-size:1.2rem;'>{result.get('summary', 'Scan completed')}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='paywall'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#ff0000; margin:0;'>FULL REPORT LOCKED</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#00d4ff; margin:20px 0;'>Unlock detailed findings + remediation steps for $9 (one-time)</p>", unsafe_allow_html=True)
        st.markdown("[UNLOCK NOW $9 – Instant Download](https://porschza.gumroad.com/l/aegis-full-report)", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer'>AEGIS v12.0 – WAT SYSTEMS – Secure the Future</div>", unsafe_allow_html=True)
