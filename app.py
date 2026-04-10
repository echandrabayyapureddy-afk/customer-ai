import streamlit as st
import google.generativeai as genai

# 🔐 Add your Gemini API key here
genai.configure(api_key="YOUR_API_KEY_HERE")

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Customer AI", page_icon="🤖")
st.title("🤖 Customer Frustration Intelligence Engine")

st.markdown("AI-powered analysis using Gemini")

text = st.text_area("Enter customer message:")

if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please enter a message")
    else:
        prompt = f"""
        Analyze the following customer message:

        "{text}"

        Give output in this format:
        Emotion:
        Confidence Score (0 to 1):
        Urgency (High/Medium/Low):
        Priority Score (calculate using: score × weight where High=3, Medium=2, Low=1):
        Suggested Response:
        """

        response = model.generate_content(prompt)
        output = response.text

        st.subheader("📊 AI Analysis")
        st.write(output)

        st.info("Powered by Gemini AI")
