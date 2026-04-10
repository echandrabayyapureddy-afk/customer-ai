import streamlit as st
import google.generativeai as genai

# ✅ Configure API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ USE THIS MODEL (this WILL work)
model = genai.GenerativeModel("gemini-pro")

st.title("🤖 Customer Frustration Intelligence Engine")

text = st.text_area("Enter customer message:")


def fallback(text):
    text = text.lower()

    if "harass" in text or "touch" in text or "die" in text:
        return "Critical", 1.0, "High", 3
    elif "bad" in text or "angry" in text:
        return "Angry", 0.8, "High", 3
    else:
        return "Neutral", 0.5, "Low", 1


if st.button("Analyze"):
    try:
        prompt = f"Analyze sentiment and urgency: {text}"
        response = model.generate_content(prompt)

        st.subheader("Gemini Output")
        st.write(response.text)

    except Exception as e:
        st.subheader("Fallback Mode Activated")
        st.error(str(e))

        emotion, score, urgency, weight = fallback(text)
        priority = score * weight

        st.write(f"Emotion: {emotion}")
        st.write(f"Score: {score}")
        st.write(f"Urgency: {urgency}")
        st.write(f"Priority: {priority}")
