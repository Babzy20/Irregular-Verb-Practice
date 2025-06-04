import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache_data
def load_verbs():
    return pd.read_csv('verbs.csv')

verbs_df = load_verbs()

# Initialize session state
if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]

if 'badges' not in st.session_state:
    st.session_state.badges = []

if 'reminders' not in st.session_state:
    st.session_state.reminders = []

# Define badges and reminders
badges = [
    {"name": "First Correct Answer", "emoji": "🏅"},
    {"name": "Five Correct Answers", "emoji": "🥇"},
    {"name": "Ten Correct Answers", "emoji": "🥈"},
    {"name": "Twenty Correct Answers", "emoji": "🥉"}
]

reminders = [
    {"name": "Keep Going!", "emoji": "💪", "description": "You're doing great! Keep practicing."},
    {"name": "Almost There!", "emoji": "👍", "description": "Just a few more correct answers to earn a badge."},
    {"name": "You Can Do It!", "emoji": "🙌", "description": "Believe in yourself and keep trying."}
]

# Function to check answers
def check_answers(base_form, simple_past, past_participle):
    match = verbs_df[verbs_df['Base Form'] == base_form]
    if match.empty:
        return False, {"Simple Past": "N/A", "Past Participle": "N/A"}
    correct = match.iloc[0]
    return (correct['Simple Past'] == simple_past and correct['Past Participle'] == past_participle), correct

# Layout with two columns
col1, col2 = st.columns([1, 2])  # Left (narrow), Right (wider)

with col1:
    st.header("🏅 Achievements")
    for badge in badges:
        status = "✅" if badge["name"] in st.session_state.badges else "🔒"
        st.markdown(f"{badge['emoji']} **{badge['name']}** - {status}")

    st.header("😬 Reminders")
    for reminder in reminders:
        if reminder["name"] in st.session_state.reminders:
            st.markdown(f"{reminder['emoji']} **{reminder['name']}** - {reminder['description']}")
        else:
            st.markdown(f"{reminder['emoji']} **{reminder['name']}** - 🔒")

with col2:
    st.header("🎯 Single Verb Quiz")
    if st.button("🔄 New Verb"):
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]
    verb = st.session_state.current_verb
    st.write(f"Base Form: **{verb['Base Form']}**")
    simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
    past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")
    if st.button("✅ Submit"):
        correct, correct_forms = check_answers(verb['Base Form'], simple_past, past_participle)
        if correct:
            st.success("Correct!")
            st.session_state.badges.append("First Correct Answer")
        else:
            st.error("Incorrect!")
            st.write(f"Correct Simple Past: {correct_forms['Simple Past']}")
            st.write(f"Correct Past Participle: {correct_forms['Past Participle']}")

# Save the updated code to a file
with open('updated_app.py', 'w') as f:
    f.write("""
import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache_data
def load_verbs():
    return pd.read_csv('verbs.csv')

verbs_df = load_verbs()

# Initialize session state
if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]

if 'badges' not in st.session_state:
    st.session_state.badges = []

if 'reminders' not in st.session_state:
    st.session_state.reminders = []

# Define badges and reminders
badges = [
    {"name": "First Correct Answer", "emoji": "🏅"},
    {"name": "Five Correct Answers", "emoji": "🥇"},
    {"name": "Ten Correct Answers", "emoji": "🥈"},
    {"name": "Twenty Correct Answers", "emoji": "🥉"}
]

reminders = [
    {"name": "Keep Going!", "emoji": "💪", "description": "You're doing great! Keep practicing."},
    {"name": "Almost There!", "emoji": "👍", "description": "Just a few more correct answers to earn a badge."},
    {"name": "You Can Do It!", "emoji": "🙌", "description": "Believe in yourself and keep trying."}
]

# Function to check answers
def check_answers(base_form, simple_past, past_participle):
    match = verbs_df[verbs_df['Base Form'] == base_form]
    if match.empty:
        return False, {"Simple Past": "N/A", "Past Participle": "N/A"}
    correct = match.iloc[0]
    return (correct['Simple Past'] == simple_past and correct['Past Participle'] == past_participle), correct

# Layout with two columns
col1, col2 = st.columns([1, 2])  # Left (narrow), Right (wider)

with col1:
    st.header("🏅 Achievements")
    for badge in badges:
        status = "✅" if badge["name"] in st.session_state.badges else "🔒"
        st.markdown(f"{badge['emoji']} **{badge['name']}** - {status}")

    st.header("😬 Reminders")
    for reminder in reminders:
        if reminder["name"] in st.session_state.reminders:
            st.markdown(f"{reminder['emoji']} **{reminder['name']}** - {reminder['description']}")
        else:
            st.markdown(f"{reminder['emoji']} **{reminder['name']}** - 🔒")

with col2:
    st.header("🎯 Single Verb Quiz")
    if st.button("🔄 New Verb"):
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]
    verb = st.session_state.current_verb
    st.write(f"Base Form: **{verb['Base Form']}**")
    simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
    past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")
    if st.button("✅ Submit"):
        correct, correct_forms = check_answers(verb['Base Form'], simple_past, past_participle)
        if correct:
            st.success("Correct!")
            st.session_state.badges.append("First Correct Answer")
        else:
            st.error("Incorrect!")
            st.write(f"Correct Simple Past: {correct_forms['Simple Past']}")
            st.write(f"Correct Past Participle: {correct_forms['Past Participle']}")
""")

print("The updated code has been saved to 'updated_app.py'.")

