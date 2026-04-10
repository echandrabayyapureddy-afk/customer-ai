import streamlit as st
import requests
import time

API_KEY = st.secrets["GEMINI_API_KEY"]

# 🎨 PAGE CONFIG
st.set_page_config(page_title="Customer AI", page_icon="🤖", layout="centered")

# 🌈 CUSTOM CSS (ANIMATIONS + UI)
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    color: white;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    animation: fadeIn 2s ease-in-out;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #ddd;
    animation: fadeIn 3s ease-in-out;
}

.card {
    background: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    animation: slideUp 1s ease-in-out;
    margin-top: 15px;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes slideUp {
    from {transform: translateY(40px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# 🎯 TITLE
st.markdown("<div class='title'>🤖 Customer Frustration Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered sentiment & priority analysis</div>", unsafe_allow_html=True)

# 📥 INPUT
text = st.text_area("💬 Enter customer message:", height=150)


# 🔁 FALLBACK
def fallback_analysis(text):
    text = text.lower()

    if any(word in text for word in ["harass", "abuse", "touch", "die"]):
        return "Critical Distress", 100, "High", 3, "Immediate action required"
    elif any(word in text for word in ["angry", "bad", "worst"]):
        return "Anger", 85, "High", 3, "We sincerely apologize. Issue prioritized."
    elif any(word in text for word in ["sad", "disappointed"]):
        return "Sadness", 65, "Medium", 2, "We understand your concern."
    else:
        return "Neutral", 40, "Low", 1, "Thank you for your message."


# 🚀 BUTTON
if st.button("🚀 Analyze Now"):

    if text.strip() == "":
        st.warning("⚠️ Please enter a message")

    else:
        with st.spinner("Analyzing with AI... 🤖"):
            try:
                time.sleep(2)

                # Get model
                model_list_url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
                model_response = requests.get(model_list_url).json()
                model_name = model_response["models"][0]["name"]

                url = f"https://generativelanguage.googleapis.com/v1/{model_name}:generateContent?key={API_KEY}"

                payload = {
                    "contents": [
                        {"parts": [{"text": f"Analyze sentiment and urgency:\n{text}"}]}
                    ]
                }

                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    output = data["candidates"][0]["content"]["parts"][0]["text"]

                    st.success("🤖 Using Gemini AI")

                    st.markdown(f"<div class='card'>{output}</div>", unsafe_allow_html=True)

                else:
                    raise Exception(response.text)

            except:
                st.warning("⚠️ Fallback Mode Activated")

                emotion, score, urgency, weight, resp = fallback_analysis(text)
                priority = score * weight

                # 🎯 METRICS
                col1, col2, col3 = st.columns(3)

                col1.metric("🧠 Emotion", emotion)
                col2.metric("📊 Score", f"{score}/100")
                col3.metric("⚡ Urgency", urgency)

                # 🚨 Animated Progress
                st.markdown("### 🚨 Priority Level")
                progress = 0
                bar = st.progress(0)

                for i in range(int(priority)):
                    progress += 1
                    bar.progress(min(progress / 300, 1.0))
                    time.sleep(0.01)

                st.write(f"**Priority Score:** {priority}/300")

                # 🧮 Formula
                st.markdown("### 🧮 Calculation")
                st.code("Priority = Score × Weight")
                st.write(f"{score} × {weight} = {priority}")

                # 💬 Response
                st.markdown("### 💬 Suggested Response")
                st.success(resp)
