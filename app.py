import streamlit as st
import pandas as pd

# Load the CSV files
verbs_df = pd.read_csv('verbs.csv')
reminders_df = pd.read_csv('reminders.csv')

# Initialize session state variables
for key in ['score', 'attempts', 'streak', 'badges', 'mistakes', 'reminders']:
    if key not in st.session_state:
        st.session_state[key] = 0 if key in ['score', 'attempts', 'streak'] else []

# Function to check answers
def check_answers(base_form, simple_past, past_participle):
    correct = verbs_df[verbs_df['Base Form'] == base_form].iloc[0]
    is_correct = (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    )
    return is_correct, correct

# Function to check reminders
def check_reminders(base_form, simple_past, past_participle):
    new_reminders = []
    for _, row in reminders_df.iterrows():
        trigger = row['trigger']
        if trigger == "feel_fall" and (simple_past in ["fell", "felt"] or past_participle in ["fallen", "felt"]):
            new_reminders.append(row)
        elif trigger == "writting_writen" and (simple_past == "writting" or past_participle == "writen"):
            new_reminders.append(row)
        elif trigger == "catched" and (simple_past == "catched" or past_participle == "catched"):
            new_reminders.append(row)
        elif trigger == "teach_think" and (simple_past in ["taught", "thought"] or past_participle in ["taught", "thought"]):
            new_reminders.append(row)
        elif trigger == "5_mistakes_in_a_row" and len(st.session_state.mistakes) >= 5:
            new_reminders.append(row)
        elif trigger == "repeat_mistake" and st.session_state.mistakes.count({
            "base_form": base_form,
            "simple_past": simple_past,
            "past_participle": past_participle
        }) > 1:
            new_reminders.append(row)
    return new_reminders

# Function to check badges
def check_badges(streak):
    badge_list = [
        {"name": "No more a novice!", "emoji": "🙌", "trigger": 1, "description": "You got your first one right!"},
        {"name": "Five star!", "emoji": "⭐⭐⭐⭐⭐", "trigger": 5, "description": "You're on a roll! 5 in a row!"},
        {"name": "As great as ninTENdo", "emoji": "😅", "trigger": 10, "description": "10 in a row? Let's go!"}
    ]
    new_badges = []
    for badge in badge_list:
        if streak >= badge["trigger"] and badge["name"] not in st.session_state.badges:
            st.session_state.badges.append(badge["name"])
            new_badges.append(badge)
    return new_badges

# App layout
st.title("📚 Irregular Verbs Practice")

mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

# Grid Mode
if mode == "Grid Mode":
    st.header("🧩 Grid Mode")
    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(10).reset_index(drop=True)

    check_pressed = st.button("🔍 Check All")
    for i, row in st.session_state.grid_verbs.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
        with col1:
            st.markdown(f"**{row['Base Form']}**")
        with col2:
            sp = st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
        with col3:
            pp = st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")
        if check_pressed:
            is_correct, correct = check_answers(row['Base Form'], sp, pp)
            st.session_state.attempts += 1
            if is_correct:
                st.session_state.score += 1
                st.session_state.streak += 1
                with col4:
                    st.success("✓")
            else:
                st.session_state.streak = 0
                with col4:
                    st.error(f"{correct['Simple Past']}, {correct['Past Participle']}")
                st.session_state.mistakes.append({
                    "base_form": row['Base Form'],
                    "simple_past": sp,
                    "past_participle": pp
                })
                for reminder in check_reminders(row['Base Form'], sp, pp):
                    st.toast(f"⚠️ Reminder: {reminder['emoji']} {reminder['name']} - {reminder['description']}")
            for badge in check_badges(st.session_state.streak):
                st.toast(f"🎉 New Badge: {badge['emoji']} {badge['name']} - {badge['description']}")

    if st.button("🔁 New Verbs"):
        st.session_state.grid_verbs = verbs_df.sample(10).reset_index(drop=True)

# Single Verb Quiz Mode
elif mode == "Single Verb Quiz":
    st.header("🎯 Single Verb Quiz")
    if "current_verb" not in st.session_state:
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    verb = st.session_state.current_verb
    st.markdown(f"**Base Form:** {verb['Base Form']}")

    simple_past = st.text_input("Simple Past", key="single_sp")
    past_participle = st.text_input("Past Participle", key="single_pp")

    if st.button("Check Answer"):
        is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
        st.session_state.attempts += 1
        if is_correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
            st.session_state.streak += 1
        else:
            st.error(f"❌ Correct Answer: {correct['Simple Past']}, {correct['Past Participle']}")
            st.session_state.streak = 0
            st.session_state.mistakes.append({
                "base_form": verb['Base Form'],
                "simple_past": simple_past,
                "past_participle": past_participle
            })
            for reminder in check_reminders(verb['Base Form'], simple_past, past_participle):
                st.toast(f"⚠️ Reminder: {reminder['emoji']} {reminder['name']} - {reminder['description']}")

        for badge in check_badges(st.session_state.streak):
            st.toast(f"🎉 New Badge: {badge['emoji']} {badge['name']} - {badge['description']}")

        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

# Sidebar
with st.sidebar:
    st.header("🏅 Achievements")
    st.write("Badges Earned:")
    for badge in st.session_state.badges:
        st.markdown(f"- {badge}")
    st.write("Reminders Triggered:")
    for reminder in st.session_state.reminders:
        st.markdown(f"- {reminder}")
