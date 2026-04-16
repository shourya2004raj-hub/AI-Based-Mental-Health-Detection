import streamlit as st
from textblob import TextBlob
import time

st.set_page_config(page_title="AI Based Mental Health Companion", page_icon="🧠", layout="wide")


if "step" not in st.session_state:
    st.session_state.step = 1

if "answers" not in st.session_state:
    st.session_state.answers = [0] * 10

if "text" not in st.session_state:
    st.session_state.text = ""


st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.title {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #cbd5f5;
}

.section {
    padding: 25px;
    border-radius: 15px;
    background-color: #1e293b;
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 10px;
    font-size: 18px;
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
}

label {
    font-size: 18px !important;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">🧠 AI Based Mental Health Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Personal Mental Health Companion</div>', unsafe_allow_html=True)

st.markdown("---")


QUESTIONS = [
    "Feeling low or sad recently?",
    "Lost interest in activities?",
    "Trouble sleeping or oversleeping?",
    "Low energy most of the day?",
    "Difficulty concentrating?",
    "Feeling anxious or restless?",
    "Avoiding people or social situations?"
]

OPTIONS = {"No": 0, "Sometimes": 1, "Yes": 2}

def classify(score):
    if score <= 4:
        return "Normal"
    elif score <= 9:
        return "Mild Stress"
    else:
        return "High Risk"

def sentiment_score(text):
    if not text.strip():
        return 0
    polarity = TextBlob(text).sentiment.polarity
    if polarity < -0.25:
        return 2
    elif polarity < 0:
        return 1
    return 0


if st.session_state.step == 1:

    st.markdown("## 🧭 Step 1: Self Assessment")

    progress = st.progress(0)

    for i, q in enumerate(QUESTIONS):
        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.markdown(f"### {q}")
        ans = st.radio(
            "",
            list(OPTIONS.keys()),
            key=f"q{i}",
            horizontal=True
        )

        st.session_state.answers[i] = OPTIONS[ans]

        st.markdown('</div>', unsafe_allow_html=True)

        progress.progress((i + 1) / len(QUESTIONS))

    if st.button("Next ➡️"):
        st.session_state.step = 2


elif st.session_state.step == 2:

    st.markdown("## 💬 Step 2: Your Feelings")

    text = st.text_area("How are you feeling today?", height=150)
    st.session_state.text = text

    if st.button("Analyze ➡️"):
        st.session_state.step = 3


elif st.session_state.step == 3:

    st.markdown("## 📊 Step 3: Results")

    with st.spinner("Analyzing your mental state... 🤖"):
        time.sleep(2)

        question_score = sum(st.session_state.answers)
        extra = sentiment_score(st.session_state.text)
        total = question_score + extra
        result = classify(total)

    st.metric("Total Score", total)

    if result == "Normal":
        st.success("🟢 You are doing well")
    elif result == "Mild Stress":
        st.warning("🟡 Mild stress detected")
    else:
        st.error("🔴 High stress detected")

    st.markdown("### 💡 Suggestions")

    if result == "Normal":
        st.write("- You appear to be maintaining a stable and healthy mental state. Continue following a balanced daily routine.")
        st.write("- Stay physically active and engage in activities that help you relax and feel positive.")
        st.write("- Maintain regular social interactions with friends, family, or peers to support emotional well-being.")

    elif result == "Mild Stress":
        st.write("- Your responses indicate some level of stress. Try to take regular breaks and avoid overloading yourself.")
        st.write("- Consider practicing relaxation techniques such as deep breathing, meditation, or light exercise.")
        st.write("- It may help to talk to someone you trust, such as a friend, family member, or mentor.")

    else:
        st.write("- Your responses suggest a higher level of stress and should be taken seriously.")
        st.write("- Try to speak openly with someone you trust and avoid dealing with these feelings alone.")
        st.write("- It is recommended to consult a qualified professional for proper guidance and support.")
    st.markdown("---")

    if st.button("🔄 Start Again"):
        st.session_state.step = 1