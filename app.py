import streamlit as st
import pandas as pd
import random

# Load the CSV file
verbs_df = pd.read_csv('verbs 2.csv')

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

# Define badges and reminders
badges = [
    {"emoji": "🥇", "name": "First Correct Answer", "description": "Get your first correct answer"},
    {"emoji": "🏅", "name": "5 Correct Answers", "description": "Get 5 correct answers in a row"},
    {"emoji": "🏆", "name": "10 Correct Answers", "description": "Get 10 correct answers in a row"}
]

reminders = [
    {"emoji": "😬", "name": "Common Mistake: Catched", "description": "Remember, the correct form is 'caught'"},
    {"emoji": "😬", "name": "Common Mistake: Feel vs. Fall", "description": "Don't confuse 'feel' with 'fall'"}
]

# Function to check answers and update score
def check_answer(base, past, participle):
    correct_past = verbs_df.loc[verbs_df['Base Form'] == base, 'Simple Past'].values[0]
    correct_participle = verbs_df.loc[verbs_df['Base Form'] == base, 'Past Participle'].values[0]
    if past == correct_past and participle == correct_participle:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.attempts += 1
        if st.session_state.streak == 1 and "First Correct Answer" not in st.session_state.badges:
            st.session_state.badges.append("First Correct Answer")
        if st.session_state.streak == 5 and "5 Correct Answers" not in st.session_state.badges:
            st.session_state.badges.append("5 Correct Answers")
        if st.session_state.streak == 10 and "10 Correct Answers" not in st.session_state.badges:
            st.session_state.badges.append("10 Correct Answers")
        return True
    else:
        st.session_state.streak = 0
        st.session_state.attempts += 1
        if past == "catched" and "Common Mistake: Catched" not in st.session_state.reminders:
            st.session_state.reminders.append("Common Mistake: Catched")
        if base == "feel" and participle == "fallen" and "Common Mistake: Feel vs. Fall" not in st.session_state.reminders:
            st.session_state.reminders.append("Common Mistake: Feel vs. Fall")
        return False

# Function to reset progress
def reset_progress():
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.streak = 0
    st.session_state.badges = []
    st.session_state.reminders = []

# Sidebar for achievements and reminders
with st.sidebar:
    st.header("🏅 Achievements")
    badge_table = []
    for badge in badges:
        status = "✅ Earned" if badge["name"] in st.session_state.badges else "🔒 Locked"
        badge_table.append([badge["emoji"], badge["name"], badge["description"], status])
    st.table(pd.DataFrame(badge_table, columns=["Icon", "Badge Name", "Description", "Status"]))

    st.header("😬 Reminders: Learn from Your Mistakes")
    reminder_table = []
    for reminder in reminders:
        if reminder["name"] in st.session_state.reminders:
            reminder_table.append([reminder["emoji"], reminder["name"], reminder["description"], "✅ Earned"])
        else:
            reminder_table.append([reminder["emoji"], reminder["name"], "🔒 Locked"])
    if any(r["name"] in st.session_state.reminders for r in reminders):
        st.table(pd.DataFrame(reminder_table, columns=["Icon", "Reminder Name", "Description", "Status"]))
    else:
        st.table(pd.DataFrame(reminder_table, columns=["Icon", "Reminder Name", "Status"]))

# Main app
st.title("Irregular Verbs Practice Tool")

mode = st.selectbox("Choose Mode", ["Single Verb Quiz", "Grid Mode"])

if mode == "Single Verb Quiz":
    verb = random.choice(verbs_df["Base Form"].values)
    st.write(f"Verb: **{verb}**")
    past = st.text_input("Simple Past")
    participle = st.text_input("Past Participle")
    if st.button("Submit"):
        if check_answer(verb, past, participle):
            st.success("Correct!")
        else:
            st.error("Incorrect. Try again.")
    st.write(f"Score: {st.session_state.score}")
    st.write(f"Attempts: {st.session_state.attempts}")
    st.write(f"Streak: {st.session_state.streak}")
    if st.button("Reset Progress"):
        reset_progress()

elif mode == "Grid Mode":
    st.write("Fill in the forms for the following verbs:")
    verbs = random.sample(list(verbs_df["Base Form"].values), 20)
    answers = {}
    for verb in verbs:
        st.write(f"Verb: **{verb}**")
        past = st.text_input(f"Simple Past for {verb}")
        participle = st.text_input(f"Past Participle for {verb}")
        answers[verb] = (past, participle)
    if st.button("Submit All"):
        correct_count = 0
        for verb, (past, participle) in answers.items():
            if check_answer(verb, past, participle):
                correct_count += 1
        st.write(f"Correct Answers: {correct_count} out of 20")
        st.write(f"Score: {st.session_state.score}")
        st.write(f"Attempts: {st.session_state.attempts}")
        st.write(f"Streak: {st.session_state.streak}")
        if st.button("Reset Progress"):
            reset_progress()

