import streamlit as st
import pandas as pd

# Load verbs data
@st.cache_data
def load_verbs():
    return pd.read_csv('verbs.csv')

verbs_df = load_verbs()

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []
if 'mistakes' not in st.session_state:
    st.session_state.mistakes = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

# Define badges and reminders
badges = [
    {"name": "No more a novice!", "emoji": "🙌", "trigger": 1, "description": "You got your first one right!"},
    {"name": "Five star!", "emoji": "⭐⭐⭐⭐⭐", "trigger": 5, "description": "You're on a roll! 5 in a row!"},
    {"name": "As great as ninTENdo", "emoji": "😅", "trigger": 10, "description": "10 in a row? Let's go!"}
]

reminders = [
    {"name": "You have fallen for it", "emoji": "🦂", "trigger": "feel_fall", "description": "Confused forms of feel and fall"},
    {"name": "Learn how to write", "emoji": "✏️", "trigger": "wrotte_writen", "description": "'Written' is the only form with 2 Ts"},
    {"name": "You just got caught!", "emoji": "🕵️‍♂️", "trigger": "catched", "description": "Wrote 'catched'"},
    {"name": "Think it through or we'll teach you a lesson!", "emoji": "🧠", "trigger": "teach_think", "description": "Confused forms of teach and think"},
    {"name": "When times are tough", "emoji": "🍦", "trigger": "5_mistakes_in_a_row", "description": "5 mistakes in a row"},
    {"name": "Fool me twice, shame on me!", "emoji": "😤", "trigger": "repeat_mistake", "description": "Made the same mistake twice in the same session"}
]

# Check answers
def check_answers(base_form, simple_past, past_participle):
    correct = verbs_df[verbs_df['Base Form'] == base_form].iloc[0]
    return (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    ), correct

# Check badges
def check_badges(streak):
    new_badges = []
    for badge in badges:
        if streak >= badge["trigger"] and badge["name"] not in st.session_state.badges:
            st.session_state.badges.append(badge["name"])
            new_badges.append(badge)
    return new_badges

# Check reminders
def check_reminders(base_form, simple_past, past_participle):
    new_reminders = []
    mistake = {"base_form": base_form, "simple_past": simple_past, "past_participle": past_participle}
    st.session_state.mistakes.append(mistake)
    for reminder in reminders:
        trigger = reminder["trigger"]
        if trigger == "feel_fall" and (simple_past.lower() in ["fell", "felt"] or past_participle.lower() in ["fallen", "felt"]):
            pass
        elif trigger == "wrotte_writen" and (simple_past.lower() == "writting" or past_participle.lower() == "writen"):
            pass
        elif trigger == "catched" and (simple_past.lower() == "catched" or past_participle.lower() == "catched"):
            pass
        elif trigger == "teach_think" and (simple_past.lower() in ["taught", "thought"] or past_participle.lower() in ["taught", "thought"]):
            pass
        elif trigger == "5_mistakes_in_a_row" and len(st.session_state.mistakes) >= 5 and all(m["simple_past"] == "" or m["past_participle"] == "" for m in st.session_state.mistakes[-5:]):
            pass
        elif trigger == "repeat_mistake" and st.session_state.mistakes.count(mistake) > 1:
            pass
        else:
            continue
        if reminder["name"] not in st.session_state.reminders:
            st.session_state.reminders.append(reminder["name"])
            new_reminders.append(reminder)
    return new_reminders

# UI
st.title("📚 Irregular Verbs Practice")

mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

if mode == "Grid Mode":
    st.header("🧩 Grid Mode")
    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(10).reset_index(drop=True)

    for i, row in st.session_state.grid_verbs.iterrows():
        col1, col2, col3, col4 = st.columns
