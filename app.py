import streamlit as st
import requests
import time

API_KEY = st.secrets["GEMINI_API_KEY"]

# 🎨 Page config
st.set_page_config(page_title="Customer AI", page_icon="🤖", layout="centered")

# 🎯 Title
st.markdown("<h1 style='text-align: center;'>🤖 Customer Frustration Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-powered sentiment & priority analysis</p>", unsafe_allow_html=True)

# 📥 Input
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
if st.button("🔍 Analyze"):

    if text.strip() == "":
        st.warning("⚠️ Please enter a message")

    else:
        try:
            time.sleep(2)

            # 🔍 Get models
            model_list_url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
            model_response = requests.get(model_list_url).json()
            models = model_response.get("models", [])

            model_name = models[0]["name"]

            # 🔥 API call
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

                # 🎨 Output box
                st.markdown("### 📊 AI Analysis")
                st.markdown(
                    f"""
                    <div style='background-color:#1e1e1e;padding:15px;border-radius:10px'>
                    {output}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                raise Exception(response.text)

        except Exception as e:
            st.warning("⚠️ Fallback Mode Activated")

            emotion, score, urgency, weight, response = fallback_analysis(text)
            priority = score * weight

            # 🎨 METRICS UI
            col1, col2, col3 = st.columns(3)

            col1.metric("🧠 Emotion", emotion)
            col2.metric("📊 Score", f"{score}/100")
            col3.metric("⚡ Urgency", urgency)

            # 🎯 Priority Bar
            st.markdown("### 🚨 Priority Level")
            st.progress(min(priority / 300, 1.0))  # scaled

            st.write(f"**Priority Score:** {priority}/300")

            # 🧮 Formula
            st.markdown("### 🧮 Calculation")
            st.code("Priority = Score × Weight")
            st.write(f"{score} × {weight} = {priority}")

            # 💬 Response
            st.markdown("### 💬 Suggested Response")
            st.success(response)
