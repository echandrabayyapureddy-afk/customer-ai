import streamlit as st

st.title("🤖 Customer Frustration Intelligence Engine")

text = st.text_area("Enter customer message:")

if st.button("Analyze"):
    if "worst" in text.lower() or "bad" in text.lower():
        emotion = "anger"
        urgency = "High"
        response = "We apologize. Your issue is being prioritized."
    elif "disappointed" in text.lower() or "sad" in text.lower():
        emotion = "sadness"
        urgency = "Medium"
        response = "We understand your concern."
    else:
        emotion = "neutral"
        urgency = "Low"
        response = "Thank you for your feedback."

    st.write(f"Emotion: {emotion}")
    st.write(f"Urgency: {urgency}")
    st.success(response)
