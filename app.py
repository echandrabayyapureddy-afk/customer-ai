import streamlit as st
import google.generativeai as genai

# 🔐 Configure API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ✅ Use stable model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Customer AI", page_icon="🤖")
st.title("🤖 Customer Frustration Intelligence Engine")

st.markdown("AI-powered customer sentiment & priority analysis")

text = st.text_area("Enter customer message:")


# 🔁 FALLBACK FUNCTION (IMPORTANT)
def fallback_analysis(text):
    text = text.lower()

    if any(word in text for word in [
        "harass", "abuse", "assault", "touch", "unsafe",
        "kill", "die", "don't want to live", "suicide"
    ]):
        emotion = "critical distress"
        score = 1.0
        urgency = "High"
        weight = 3
        response = "We are deeply concerned. Please contact emergency support immediately."

    elif any(word in text for word in ["worst", "bad", "angry", "terrible", "hate"]):
        emotion = "anger"
        score = 0.9
        urgency = "High"
        weight = 3
        response = "We sincerely apologize. Your issue is being prioritized immediately."

    elif any(word in text for word in ["sad", "disappointed", "unhappy"]):
        emotion = "sadness"
        score = 0.7
        urgency = "Medium"
        weight = 2
        response = "We understand your concern and will resolve it soon."

    else:
        emotion = "neutral"
        score = 0.5
        urgency = "Low"
        weight = 1
        response = "Thank you for reaching out. We’ll look into it."

    priority = score * weight
    return emotion, score, urgency, weight, priority, response


# 🚀 BUTTON
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter a message")

    else:
        try:
            # 🧠 Simple prompt (less quota)
            prompt = f"""
            Classify this message:

            {text}

            Return:
            Emotion
            Score (0-1)
            Urgency (High/Medium/Low)
            Priority Score
            Response
            """

            response = model.generate_content(prompt)

            if response and response.text:
                st.subheader("🤖 AI Analysis")
                st.write(response.text)
                st.success("Using Gemini AI")

            else:
                raise Exception("Empty response")

        except Exception as e:
            # 🔁 FALLBACK MODE
            st.subheader("⚠️ Fallback Mode Activated")
            st.error(f"Gemini Error: {e}")

            emotion, score, urgency, weight, priority, response = fallback_analysis(text)

            st.write(f"**Emotion:** {emotion}")
            st.write(f"**Confidence Score:** {score:.2f}")

            if urgency == "High":
                st.error("🚨 High Urgency")
            elif urgency == "Medium":
                st.warning("⚠️ Medium Urgency")
            else:
                st.success("✅ Low Urgency")

            st.write(f"**Priority Score:** {priority:.2f}")

            # 🧮 Formula
            st.subheader("🧮 Priority Calculation")
            st.code("Priority Score = Confidence Score × Urgency Weight")
            st.write(f"= {score:.2f} × {weight}")
            st.write(f"= {priority:.2f}")

            st.subheader("💬 Suggested Response")
            st.success(response)
