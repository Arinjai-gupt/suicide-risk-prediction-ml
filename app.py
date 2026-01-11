import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Suicide Risk Predictor",
    page_icon="🧠",
    layout="centered"
)

# ---------------- FINAL DARK CSS (NO WHITE SPACES) ----------------
st.markdown("""
<style>

/* Remove default Streamlit padding & gaps */
.block-container {
    padding-top: 4.5rem !important;  
    padding-bottom: 2rem !important;
    max-width: 420px;
}


/* Remove empty containers */
.element-container:empty {
    display: none !important;
}

/* Remove separators */
hr {
    display: none !important;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0b1220, #020617);
    color: #e5e7eb;
}

/* Card */
.card {
    background: rgba(15, 23, 42, 0.95);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 0 20px rgba(99,102,241,0.12);
    margin-bottom: 18px;
}

/* Title */
.title {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    color: #e5e7eb;
    margin-bottom: 6px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #94a3b8;
    margin-bottom: 18px;
}

/* Slider labels */
label {
    font-size: 14px !important;
    font-weight: 600;
    color: #e5e7eb !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 14px;
    padding: 14px;
    font-size: 16px;
    font-weight: 700;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.02);
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #22c55e, #eab308, #ef4444);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🧠 Suicide Risk Predictor</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI-based mental health risk assessment tool</div>",
    unsafe_allow_html=True
)

# ---------------- INPUT CARD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Psychological Indicators")

depression = st.slider("😔 Depression Score", 0, 10, 5)
anxiety = st.slider("😰 Anxiety Score", 0, 10, 5)
stress = st.slider("🔥 Stress Level", 0, 10, 5)
support = st.slider("🤝 Social Support Score", 0, 10, 5)
esteem = st.slider("💪 Self-Esteem Score", 0, 10, 5)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PREDICT BUTTON ----------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Predict Risk", use_container_width=True):
    payload = {
        "Depression_Score": depression,
        "Anxiety_Score": anxiety,
        "Stress_Level": stress,
        "Social_Support_Score": support,
        "Self_Esteem_Score": esteem
    }

    try:
        BACKEND_URL = "https://suicide-risk-prediction-ml-backend.onrender.com/predict"
        response = requests.post(BACKEND_URL,json=payload,headers={"Content-Type": "application/json"},timeout=20)
        prob = response.json()["suicide_risk_probability"]

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈 Risk Assessment Result")

        st.progress(prob)

        if prob < 0.3:
            st.success(f"🟢 Low Risk ({prob:.2f})")
            st.markdown(
        "💙 **You seem to be doing relatively okay right now.**  \n"
        "That doesn’t mean your feelings don’t matter — they absolutely do.  \n"
        "Keep taking care of yourself, stay connected with people you trust, "
        "and don’t hesitate to reach out if things ever start feeling heavy."
        )
        elif prob < 0.6:
            st.warning(f"🟡 Moderate Risk ({prob:.2f})")
            st.markdown(
        "🫂 **It looks like you may be going through a tough time.**  \n"
        "You’re not weak for feeling this way — stress and emotions can build up silently.  \n"
        "Talking to someone you trust or taking small steps toward support "
        "could really help lighten the load."
        )
        else:
            st.error(f"🔴 High Risk ({prob:.2f})")
            st.markdown(
        "❤️ **You’re not alone — and what you’re feeling matters deeply.**  \n"
        "If things feel overwhelming right now, please know that help is available "
        "and people genuinely care about you.  \n\n"
        "🆘 **If you can, please consider reaching out to a trusted person or a mental health professional right now.**  \n"
        "If you’re in immediate danger, contacting local emergency services or a suicide prevention helpline can make a real difference."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    except:
        st.error("🚫 Backend not reachable. Please ensure FastAPI is running.")
        
