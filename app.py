import streamlit as st
import pandas as pd

# Load verbs data
verbs = pd.read_csv('verbs.csv')

# Load achievements and reminders data
achievements = pd.read_csv('achievements.csv')
reminders = pd.read_csv('reminders.csv')

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

# Function to check answers and update score
def check_answers(base_form, simple_past, past_participle):
    correct = verbs[(verbs['Base Form'] == base_form) & 
                    (verbs['Simple Past'] == simple_past) & 
                    (verbs['Past Participle'] == past_participle)]
    if not correct.empty:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.attempts += 1
        return True
    else:
        st.session_state.streak = 0
        st.session_state.attempts += 1
        return False

# Function to check and award badges
def check_badges():
    for _, badge in achievements.iterrows():
        if badge['trigger'] == 'streak' and st.session_state.streak >= int(badge['trigger_value']):
            if badge['name'] not in st.session_state.badges:
                st.session_state.badges.append(badge['name'])

# Function to check reminders
def check_reminders(simple_past, past_participle):
    for _, reminder in reminders.iterrows():
        if reminder['trigger'] == 'writting_writen' and (simple_past.lower() == 'wrotte' or past_participle.lower() == 'writen'):
            if reminder['name'] not in st.session_state.reminders:
                st.session_state.reminders.append(reminder['name'])

# Sidebar for achievements and reminders
with st.sidebar:
    st.header("🏅 Achievements")
    badge_table = []
    for _, badge in achievements.iterrows():
        if badge['name'] in st.session_state.badges:
            badge_table.append([badge['emoji'], badge['name'], badge['description'], "✅ Earned"])
        else:
            badge_table.append([badge['emoji'], badge['name'], badge['description'], "🔒"])
    st.table(pd.DataFrame(badge_table, columns=["Icon", "Badge Name", "Description", "Status"]).style.hide(axis='index'))

    st.header("😬 Reminders: Learn from Your Mistakes")
    reminder_table = []
    for _, reminder in reminders.iterrows():
        if reminder['name'] in st.session_state.reminders:
            reminder_table.append([reminder['emoji'], reminder['name'], reminder['description'], "✅ Earned"])
        else:
            reminder_table.append([reminder['emoji'], reminder['name'], reminder['description'], "🔒"])
    st.table(pd.DataFrame(reminder_table, columns=["Icon", "Reminder Name", "Description", "Status"]).style.hide(axis='index'))

# Main app
st.title("Irregular Verbs Practice")

mode = st.selectbox("Choose Mode", ["Single Verb", "Grid Mode"])

if mode == "Single Verb":
    st.header("Single Verb Quiz")
    verb = verbs.sample().iloc[0]
    st.write(f"Base Form: **{verb['Base Form']}**")
    simple_past = st.text_input("Simple Past")
    past_participle = st.text_input("Past Participle")
    if st.button("Submit"):
        if check_answers(verb['Base Form'], simple_past, past_participle):
            st.success("Correct!")
        else:
            st.error("Incorrect!")
        check_badges()
        check_reminders(simple_past, past_participle)

elif mode == "Grid Mode":
    st.header("Grid Mode")
    grid_verbs = verbs.sample(10)
    for i, row in grid_verbs.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
        with col1:
            st.markdown(f"**{row['Base Form']}**")
        with col2:
            simple_past = st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
        with col3:
            past_participle = st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")
        user_inputs[row['Base Form']] = {
            'simple_past': simple_past,
            'past_participle': past_participle


# Display score
st.write(f"Score: {st.session_state.score}")
st.write(f"Attempts: {st.session_state.attempts}")
st.write(f"Streak: {st.session_state.streak}")
