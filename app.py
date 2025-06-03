import streamlit as st
import pandas as pd

# Load the list of irregular verbs
@st.cache_data
def load_verbs():
    return pd.read_csv('verbs.csv')

verbs_df = load_verbs()

# Function to check answers
def check_answers(base_form, simple_past, past_participle):
    correct = verbs_df[verbs_df['Base Form'] == base_form].iloc[0]
    return (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    ), correct

# Initialize session state
if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []

# Define badges
badges = [
    {"name": "No more a novice!", "emoji": "🙌", "trigger": 1, "description": "You got your first one right!"},
    {"name": "Five star!", "emoji": "⭐⭐⭐⭐⭐", "trigger": 5, "description": "You're on a roll! 5 in a row!"},
    {"name": "As great as ninTENdo", "emoji": "😅", "trigger": 10, "description": "10 in a row? You're a legend!"}
]

# Function to check and award badges
def check_badges(streak):
    new_badges = []
    for badge in badges:
        if streak >= badge["trigger"] and badge["name"] not in st.session_state.badges:
            st.session_state.badges.append(badge["name"])
            new_badges.append(badge)
    return new_badges

# App title
st.title("📚 Irregular Verbs Practice")

# Mode selection
mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

if mode == "Single Verb Quiz":
    st.header("🎯 Single Verb Quiz")

    if st.button("🔄 New Verb"):
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    verb = st.session_state.current_verb
    st.write(f"Base Form: **{verb['Base Form']}**")

    simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
    past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")

    if st.button("✅ Submit"):
        st.session_state.attempts += 1
        is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
        if is_correct:
            st.session_state.score += 1
            st.session_state.streak += 1
            st.success("Correct! Well done!")
            new_badges = check_badges(st.session_state.streak)
            if new_badges:
                st.balloons()
                for badge in new_badges:
                    st.toast(f"🎉 New Badge Earned: {badge['emoji']} {badge['name']} - {badge['description']}")
        else:
            st.session_state.streak = 0
            st.error("Incorrect.")
            st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

elif mode == "Grid Mode":
    st.header("🧩 Grid Mode")
    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

    user_inputs = []
    show_answers = st.button("🔍 Check All")

    st.write("### Fill in the forms:")
    for i, row in st.session_state.grid_verbs.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
        with col1:
            st.markdown(f"**{row['Base Form']}**")
        with col2:
            simple_past = st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
        with col3:
            past_participle = st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")
        with col4:
            if show_answers:
                is_correct, correct = check_answers(row['Base Form'], simple_past, past_participle)
                if is_correct:
                    st.success("✓")
                else:
                    st.error(f"{correct['Simple Past']}, {correct['Past Participle']}")
        user_inputs.append((row['Base Form'], simple_past, past_participle))

    if st.button("🆕 New Verbs"):
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

if st.button("🔁 Reset Score"):
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.streak = 0
    st.session_state.badges = []

# Display badge board
st.header("🏅 Achievements")
badge_table = []
for badge in badges:
    status = "✅ Earned" if badge["name"] in st.session_state.badges else "🔒 Locked"
    badge_table.append([badge["emoji"], badge["name"], badge["description"], status])

st.table(pd.DataFrame(badge_table, columns=["Icon", "Badge Name", "Description", "Status"]))
