import streamlit as st
import time
import requests

# 🔐 API KEY
API_KEY = st.secrets["GEMINI_API_KEY"]

# 🎨 UI
st.set_page_config(page_title="Customer AI", page_icon="🤖")
st.title("🤖 Customer Frustration Intelligence Engine")
st.markdown("AI-powered customer sentiment & priority analysis")

text = st.text_area("Enter customer message:")


# 🔁 FALLBACK
def fallback_analysis(text):
    text = text.lower()

    if any(word in text for word in ["harass", "abuse", "touch", "die"]):
        return "critical distress", 1.0, "High", 3
    elif "angry" in text or "bad" in text:
        return "anger", 0.8, "High", 3
    else:
        return "neutral", 0.5, "Low", 1


# 🚀 ANALYZE
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Enter a message")

    else:
        try:
            time.sleep(2)

            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-flash-latest:generateContent?key={API_KEY}"

            payload = {
                "contents": [
                    {"parts": [{"text": f"Analyze sentiment and urgency:\n{text}"}]}
                ]
            }

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                output = data["candidates"][0]["content"]["parts"][0]["text"]

                st.subheader("🤖 Gemini AI Output")
                st.success("Using Gemini (latest API)")
                st.write(output)

            else:
                raise Exception(response.text)

        except Exception as e:
            st.subheader("⚠️ Fallback Mode Activated")
            st.error(f"Gemini Error: {e}")

            emotion, score, urgency, weight = fallback_analysis(text)
            priority = score * weight

            st.write(f"Emotion: {emotion}")
            st.write(f"Score: {score}")
            st.write(f"Urgency: {urgency}")
            st.write(f"Priority: {priority}")

            st.subheader("🧮 Formula")
            st.code("Priority = Score × Weight")
