import streamlit as st
import pandas as pd

# ----------------------------
# Helper: Achievement banner
# ----------------------------
def show_achievement_banner(message="🏆 Achievement Unlocked! 🎉"):
    st.markdown(
        f"<div style='text-align: center; font-size: 30px; color: gold;'>{message}</div>",
        unsafe_allow_html=True
    )
    st.balloons()

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_verbs():
    return pd.read_csv('verbs.csv')

@st.cache_data
def load_badges():
    df = pd.read_csv("achievements.csv")
    df['trigger'] = df['trigger'].apply(lambda x: int(x) if str(x).isdigit() else x)
    return df.to_dict(orient='records')

verbs_df = load_verbs()
badges = load_badges()

# ----------------------------
# Session state init
# ----------------------------
for key, default in {
    'score': 0,
    'attempts': 0,
    'streak': 0,
    'badges': [],
    'current_verb': None,
    'reset_inputs': False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.current_verb is None:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]

# ----------------------------
# Check logic
# ----------------------------
def check_answers(base_form, simple_past, past_participle):
    correct = verbs_df[verbs_df['Base Form'] == base_form].iloc[0]
    return (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    ), correct

def check_badges(streak=None):
    new_badges = []
    for badge in badges:
        trigger = badge["trigger"]
        if isinstance(trigger, int) and streak is not None and streak >= trigger:
            if badge["name"] not in st.session_state.badges:
                st.session_state.badges.append(badge["name"])
                new_badges.append(badge)
    return new_badges

# ----------------------------
# UI
# ----------------------------
st.title("📚 Irregular Verbs Practice")
mode = st.radio("Choose a mode:", ["Single Verb Quiz"], key="mode_selector")

if mode == "Single Verb Quiz":
    st.header("🎯 Single Verb Quiz")

    verb = st.session_state.current_verb

    st.write(f"**Base form:** {verb['Base Form']}")

    # Reset inputs if flagged
    if st.session_state.reset_inputs:
        st.session_state.user_sp = ""
        st.session_state.user_pp = ""
        st.session_state.reset_inputs = False

    user_sp = st.text_input("Simple Past", key="user_sp")
    user_pp = st.text_input("Past Participle", key="user_pp")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Check Answer"):
            is_correct, correct = check_answers(verb['Base Form'], user_sp, user_pp)
            st.session_state.attempts += 1

            if is_correct:
                st.success("Correct! ✅")
                st.session_state.score += 1
                st.session_state.streak += 1
            else:
                st.error(f"Incorrect. Correct answers: {correct['Simple Past']}, {correct['Past Participle']}")
                st.session_state.streak = 0

            # Get new verb and reset inputs safely
            st.session_state.current_verb = verbs_df.sample(1).iloc[0]
            st.session_state.reset_inputs = True

            # Check for new badges
            new_badges = check_badges(st.session_state.streak)
            for badge in new_badges:
                show_achievement_banner(f"{badge['emoji']} {badge['name']} - {badge['description']}")

            st.experimental_rerun()

    with col2:
        if st.button("🆕 New Verb"):
            st.session_state.current_verb = verbs_df.sample(1).iloc[0]
            st.session_state.reset_inputs = True
            st.experimental_rerun()

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("🏅 Achievements")
    badge_table = []
    for badge in badges:
        status = "✅ Earned" if badge["name"] in st.session_state.badges else "🔒"
        badge_table.append([badge["emoji"], badge["name"], badge["description"], status])
    st.table(pd.DataFrame(badge_table, columns=["Icon", "Badge Name", "Description", "Status"]))
