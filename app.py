import streamlit as st
import google.generativeai as genai

# 🔐 Use Streamlit secrets (recommended)
genai.configure(api_key=st.secrets["AIzaSyC5Qa_10u8pq1YdwNETv1QFfKV26qYG4qE"])

# ✅ Use lighter model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Customer AI", page_icon="🤖")
st.title("🤖 Customer Frustration Intelligence Engine")

st.markdown("AI-powered customer sentiment & priority analysis")

text = st.text_area("Enter customer message:")

# 🔁 Fallback functions
def fallback_analysis(text):
    text = text.lower()

    if any(word in text for word in ["worst", "bad", "angry", "terrible"]):
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


# 🚀 Button
if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter a message")

    else:
        try:
            # 🧠 Gemini prompt (short + efficient)
            prompt = f"""
            Analyze this customer message:

            "{text}"

            Return ONLY in this format:
            Emotion:
            Score (0-1):
            Urgency (High/Medium/Low):
            Weight (High=3, Medium=2, Low=1):
            Response:
            """

            response = model.generate_content(prompt)
            output = response.text

            st.subheader("🤖 AI Analysis")
            st.write(output)

            st.success("Using Gemini AI")

        except:
            # 🔁 FALLBACK
            st.subheader("⚠️ Fallback Mode Activated")

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

            # 🧮 Formula display
            st.subheader("🧮 Priority Calculation")
            st.code("Priority Score = Confidence Score × Urgency Weight")
            st.write(f"= {score:.2f} × {weight}")
            st.write(f"= {priority:.2f}")

            st.subheader("💬 Suggested Response")
            st.success(response)

            st.info("Fallback logic used due to API limit")
