
import streamlit as st
import pandas as pd

# Define reminders
reminders = [
    {"emoji": "🔍", "name": "Check your answers", "description": "Always review your answers before submitting."},
    {"emoji": "📝", "name": "Practice regularly", "description": "Consistency is key to mastering irregular verbs."},
    {"emoji": "📚", "name": "Use resources", "description": "Utilize available resources to improve your learning."},
]

# Initialize session state
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

# Title
st.title("Irregular Verb Practice")

# CSS for shake animation
st.markdown("""
    <style>
    .shake {
        animation: shake 0.5s;
        animation-iteration-count: 1;
    }

    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    </style>
""", unsafe_allow_html=True)

# Display reminders board
st.header("😬 Reminders: Learn from Your Mistakes")
reminder_table = []

for reminder in reminders:
    if reminder["name"] in st.session_state.reminders:
        # Show full info only if earned
        reminder_table.append([reminder["emoji"], reminder["name"], reminder["description"], "✅ Earned"])
    else:
        # Hide description entirely
        reminder_table.append([reminder["emoji"], reminder["name"], "🔒 Locked"])

# Dynamically set columns based on whether descriptions are shown
if any(r["name"] in st.session_state.reminders for r in reminders):
    st.table(pd.DataFrame(reminder_table, columns=["Icon", "Reminder Name", "Description", "Status"]))
else:
    st.table(pd.DataFrame(reminder_table, columns=["Icon", "Reminder Name", "Status"]))

# Single Verb Quiz
st.header("Single Verb Quiz")
verb = st.selectbox("Choose a verb", ["be", "have", "do", "say", "go", "get", "make", "know", "think"])
simple_past = st.text_input("Simple Past")
past_participle = st.text_input("Past Participle")

if st.button("✅ Submit"):
    correct = {"be": {"Simple Past": "was/were", "Past Participle": "been"},
               "have": {"Simple Past": "had", "Past Participle": "had"},
               "do": {"Simple Past": "did", "Past Participle": "done"},
               "say": {"Simple Past": "said", "Past Participle": "said"},
               "go": {"Simple Past": "went", "Past Participle": "gone"},
               "get": {"Simple Past": "got", "Past Participle": "gotten"},
               "make": {"Simple Past": "made", "Past Participle": "made"},
               "know": {"Simple Past": "knew", "Past Participle": "known"},
               "think": {"Simple Past": "thought", "Past Participle": "thought"}}

    if simple_past == correct[verb]["Simple Past"] and past_participle == correct[verb]["Past Participle"]:
        st.success("Correct!")
        st.session_state.streak += 1
    else:
        st.session_state.streak = 0
        st.markdown('<div class="shake"><p style="color:red; font-weight:bold;">❌ Incorrect!</p></div>', unsafe_allow_html=True)
        st.info(f"Correct forms: Simple Past - {correct[verb]['Simple Past']}, Past Participle - {correct[verb]['Past Participle']}")

# Grid Mode
st.header("Grid Mode")
verbs = ["be", "have", "do", "say", "go", "get", "make", "know", "think"]
simple_pasts = [st.text_input(f"{verb} - Simple Past") for verb in verbs]
past_participles = [st.text_input(f"{verb} - Past Participle") for verb in verbs]

if st.button("✅ Submit Grid"):
    correct = {"be": {"Simple Past": "was/were", "Past Participle": "been"},
               "have": {"Simple Past": "had", "Past Participle": "had"},
               "do": {"Simple Past": "did", "Past Participle": "done"},
               "say": {"Simple Past": "said", "Past Participle": "said"},
               "go": {"Simple Past": "went", "Past Participle": "gone"},
               "get": {"Simple Past": "got", "Past Participle": "gotten"},
               "make": {"Simple Past": "made", "Past Participle": "made"},
               "know": {"Simple Past": "knew", "Past Participle": "known"},
               "think": {"Simple Past": "thought", "Past Participle": "thought"}}

    for i, verb in enumerate(verbs):
        is_correct = simple_pasts[i] == correct[verb]["Simple Past"] and past_participles[i] == correct[verb]["Past Participle"]
        if is_correct:
            st.success(f"{verb}: Correct!")
        else:
            st.markdown(f'''
                <div class="shake">
                    <p style="color:red; font-weight:bold;">❌ {verb}: {correct[verb]['Simple Past']}, {correct[verb]['Past Participle']}</p>
                </div>
            ''', unsafe_allow_html=True)
