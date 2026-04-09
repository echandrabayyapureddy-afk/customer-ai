import streamlit as st

# Title
st.set_page_config(page_title="Customer AI", page_icon="🤖")
st.title("🤖 Customer Frustration Intelligence Engine")

st.markdown("Analyze customer messages and prioritize responses intelligently.")

# Input
text = st.text_area("Enter customer message:")

# Functions
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["worst", "bad", "angry", "terrible", "hate"]):
        return "anger", 0.9
    elif any(word in text for word in ["sad", "disappointed", "unhappy", "poor"]):
        return "sadness", 0.7
    elif any(word in text for word in ["great", "good", "love", "excellent"]):
        return "joy", 0.8
    else:
        return "neutral", 0.5

def get_urgency(emotion):
    if emotion == "anger":
        return "High"
    elif emotion == "sadness":
        return "Medium"
    else:
        return "Low"

def get_priority(score, urgency):
    if urgency == "High":
        return score * 3
    elif urgency == "Medium":
        return score * 2
    else:
        return score

def generate_response(emotion):
    if emotion == "anger":
        return "We sincerely apologize. Your issue is being prioritized immediately."
    elif emotion == "sadness":
        return "We understand your concern and will resolve it soon."
    elif emotion == "joy":
        return "We're glad you're happy! Thank you for your feedback."
    else:
        return "Thank you for reaching out. We’ll look into it."

# Button
if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please enter a message")
    else:
        emotion, score = detect_emotion(text)
        urgency = get_urgency(emotion)
        priority = get_priority(score, urgency)
        response = generate_response(emotion)

        st.subheader("📊 Analysis Result")

        st.write(f"**Emotion:** {emotion}")
        st.write(f"**Confidence Score:** {score:.2f}")

        if urgency == "High":
            st.error("🚨 High Urgency")
        elif urgency == "Medium":
            st.warning("⚠️ Medium Urgency")
        else:
            st.success("✅ Low Urgency")

        st.write(f"**Priority Score:** {priority:.2f}")

        st.subheader("💬 Suggested Response")
        st.success(response)
