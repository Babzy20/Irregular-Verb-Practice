import streamlit as st
import pandas as pd
import random

# Load the verbs from the CSV file
verbs_df = pd.read_csv("verbs.csv")

# Initialize session state variables
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "badges" not in st.session_state:
    st.session_state.badges = []
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# Define badges and reminders
badges = [
    {"name": "First Correct", "emoji": "🥇", "description": "Get your first verb correct!"},
    {"name": "Five in a Row", "emoji": "🏅", "description": "Get five verbs correct in a row!"},
    {"name": "Ten in a Row", "emoji": "🏆", "description": "Get ten verbs correct in a row!"},
]

reminders = [
    {"name": "Catched Mistake", "emoji": "😬", "description": "Remember, the past tense of 'catch' is 'caught', not 'catched'."},
    {"name": "Feel vs Fall", "emoji": "😬", "description": "Don't confuse 'feel' with 'fall'."},
]

# Function to check the user's answer
def check_answer(verb, past, participle):
    correct_past = verbs_df.loc[verbs_df["base"] == verb, "past"].values[0]
    correct_participle = verbs_df.loc[verbs_df["base"] == verb, "participle"].values[0]
    return past == correct_past and participle == correct_participle

# Function to update badges and reminders
def update_badges_and_reminders():
    if st.session_state.streak == 1 and "First Correct" not in st.session_state.badges:
        st.session_state.badges.append("First Correct")
    if st.session_state.streak == 5 and "Five in a Row" not in st.session_state.badges:
        st.session_state.badges.append("Five in a Row")
    if st.session_state.streak == 10 and "Ten in a Row" not in st.session_state.badges:
        st.session_state.badges.append("Ten in a Row")
    if "catched" in st.session_state.reminders:
        st.session_state.reminders.append("Catched Mistake")
    if "feel" in st.session_state.reminders and "fall" in st.session_state.reminders:
        st.session_state.reminders.append("Feel vs Fall")

# Main app
st.title("Irregular Verbs Practice Tool")

mode = st.selectbox("Choose a mode:", ["Single Verb Quiz", "Grid Mode"])

if mode == "Single Verb Quiz":
    verb = random.choice(verbs_df["base"].values)
    st.write(f"Verb: **{verb}**")

    past = st.text_input("Simple Past:")
    participle = st.text_input("Past Participle:")

    if st.button("Check Answer"):
        st.session_state.attempts += 1
        if check_answer(verb, past, participle):
            st.session_state.score += 1
            st.session_state.streak += 1
            st.success("Correct!")
        else:
            st.session_state.streak = 0
            st.error("Incorrect. Try again!")

        update_badges_and_reminders()

    st.write(f"Score: {st.session_state.score}")
    st.write(f"Attempts: {st.session_state.attempts}")
    st.write(f"Streak: {st.session_state.streak}")

elif mode == "Grid Mode":
    st.write("Fill in the forms for the following 20 verbs:")

    verbs = random.sample(list(verbs_df["base"].values), 20)
    past_inputs = []
    participle_inputs = []

    for verb in verbs:
        st.write(f"Verb: **{verb}**")
        past_inputs.append(st.text_input(f"Simple Past for {verb}:"))
        participle_inputs.append(st.text_input(f"Past Participle for {verb}:"))

    if st.button("Check All Answers"):
        st.session_state.attempts += 1
        correct_count = 0

        for i, verb in enumerate(verbs):
            if check_answer(verb, past_inputs[i], participle_inputs[i]):
                correct_count += 1

        st.session_state.score += correct_count
        st.session_state.streak = correct_count if correct_count == 20 else 0

        st.write(f"Correct Answers: {correct_count}/20")
        st.write(f"Score: {st.session_state.score}")
        st.write(f"Attempts: {st.session_state.attempts}")
        st.write(f"Streak: {st.session_state.streak}")

        update_badges_and_reminders()

# Display badge board in sidebar
with st.sidebar:
    st.header("🏅 Achievements")
    badge_table = []
    for badge in badges:
        status = "✅ Earned" if badge["name"] in st.session_state.badges else "🔒 Locked"
        badge_table.append([badge["emoji"], badge["name"], badge["description"], status])
    st.table(pd.DataFrame(badge_table, columns=["Icon", "Badge Name", "Description", "Status"]))

# Display reminders board in sidebar
with st.sidebar:
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


