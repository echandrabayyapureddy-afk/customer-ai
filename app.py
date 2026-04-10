import streamlit as st
import requests
import time

# 🔐 API KEY
API_KEY = st.secrets["GEMINI_API_KEY"]

# 🎨 UI
st.set_page_config(page_title="Customer AI", page_icon="🤖")
st.title("🤖 Customer Frustration Intelligence Engine")
st.markdown("AI-powered customer sentiment & priority analysis")

text = st.text_area("Enter customer message:")


# 🔁 FALLBACK FUNCTION
def fallback_analysis(text):
    text = text.lower()

    if any(word in text for word in ["harass", "abuse", "touch", "die"]):
        return "critical distress", 1.0, "High", 3
    elif any(word in text for word in ["angry", "bad", "worst"]):
        return "anger", 0.8, "High", 3
    else:
        return "neutral", 0.5, "Low", 1


# 🚀 BUTTON
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter a message")

    else:
        try:
            time.sleep(2)

            # 🔍 STEP 1: Get available models
            model_list_url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
            model_response = requests.get(model_list_url).json()

            models = model_response.get("models", [])

            if not models:
                raise Exception("No models available for this API key")

            # 👉 Pick FIRST available model automatically
            model_name = models[0]["name"]

            # 🔥 STEP 2: Use that model
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

                st.subheader("🤖 Gemini AI Output")
                st.success(f"Using model: {model_name}")
                st.write(output)

            else:
                raise Exception(response.text)

        except Exception as e:
            # 🔁 FALLBACK MODE
            st.subheader("⚠️ Fallback Mode Activated")
            st.error(f"Gemini Error: {e}")

            emotion, score, urgency, weight = fallback_analysis(text)
            priority = score * weight

            st.write(f"**Emotion:** {emotion}")
            st.write(f"**Score:** {score}")
            st.write(f"**Urgency:** {urgency}")
            st.write(f"**Priority Score:** {priority}")

            # 🧮 Formula (important for judges)
            st.subheader("🧮 Priority Calculation")
            st.code("Priority Score = Confidence Score × Urgency Weight")
            st.write(f"= {score} × {weight}")
            st.write(f"= {priority}")
