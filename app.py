import streamlit as st
import pandas as pd

# ----------------------------
# Helper: Big achievement banner
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

@st.cache_data
def load_reminders():
    return pd.read_csv("reminders.csv").to_dict(orient='records')

verbs_df = load_verbs()
badges = load_badges()
reminders = load_reminders()

# ----------------------------
# Session state init
# ----------------------------
for key, default in {
    'score': 0,
    'attempts': 0,
    'streak': 0,
    'badges': [],
    'mistakes': [],
    'reminders': [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ----------------------------
# Check logic
# ----------------------------
def check_answers(base_form, simple_past, past_participle):
    correct = verbs_df[verbs_df['Base Form'] == base_form].iloc[0]
    return (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    ), correct

def check_badges(streak=None, trigger_name=None):
    new_badges = []
    if "badges" not in st.session_state:
        st.session_state.badges = []

    for badge in badges:
        trigger = badge["trigger"]

        if isinstance(trigger, int) and streak is not None:
            if streak >= trigger and badge["name"] not in st.session_state.badges:
                st.session_state.badges.append(badge["name"])
                new_badges.append(badge)

        elif isinstance(trigger, str) and trigger_name == trigger:
            if badge["name"] not in st.session_state.badges:
                st.session_state.badges.append(badge["name"])
                new_badges.append(badge)

    return new_badges

def check_reminders(base_form, simple_past, past_participle):
    new_reminders = []
    mistake = {"base_form": base_form, "simple_past": simple_past, "past_participle": past_participle}
    st.session_state.mistakes.append(mistake)

    for reminder in reminders:
        trigger = reminder["trigger"]

        if trigger == "feel_fall" and (simple_past.lower() in ["fell", "felt"] or past_participle.lower() in ["fallen", "felt"]):
            if reminder["name"] not in st.session_state.reminders:
                st.session_state.reminders.append(reminder["name"])
                new_reminders.append(reminder)

        elif trigger == "wrotte_writen" and (simple_past.lower() == "writting" or past_participle.lower() == "writen"):
            if reminder["name"] not in st.session_state.reminders:
                st.session_state.reminders.append(reminder["name"])
                new_reminders.append(reminder)

        elif trigger == "catched" and (simple_past.lower() == "catched" or past_participle.lower() == "catched"):
            if reminder["name"] not in st.session_state.reminders:
                st.session_state.reminders.append(reminder["name"])
                new_reminders.append(reminder)

        elif trigger == "teach_think" and (simple_past.lower() in ["taught", "thought"] or past_participle.lower() in ["taught", "thought"]):
            if reminder["name"] not in st.session_state.reminders:
                st.session_state.reminders.append(reminder["name"])
                new_reminders.append(reminder)

        elif trigger == "5_mistakes_in_a_row" and len(st.session_state.mistakes) >= 5:
            last5 = st.session_state.mistakes[-5:]
            if all(m["simple_past"] == "" or m["past_participle"] == "" for m in last5):
                if reminder["name"] not in st.session_state.reminders:
                    st.session_state.reminders.append(reminder["name"])
                    new_reminders.append(reminder)

        elif trigger == "repeat_mistake" and st.session_state.mistakes.count(mistake) > 1:
            if reminder["name"] not in st.session_state.reminders:
                st.session_state.reminders.append(reminder["name"])
                new_reminders.append(reminder)

    return new_reminders

# ----------------------------
# UI
# ----------------------------
st.title("📚 Irregular Verbs Practice")
mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

if mode == "Grid Mode":
    st.header("🧩 Grid Mode")

    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(10).reset_index(drop=True)

    # If reset flag set, clear all inputs and remove the flag
    if st.session_state.get("reset_grid", False):
        for i in range(10):
            st.session_state[f"sp_{i}"] = ""
            st.session_state[f"pp_{i}"] = ""
        st.session_state["reset_grid"] = False

    if st.button("🆕 New Verbs"):
        st.session_state.grid_verbs = verbs_df.sample(10).reset_index(drop=True)
        for i in range(10):
            st.session_state[f"sp_{i}"] = ""
            st.session_state[f"pp_{i}"] = ""

    check_pressed = st.button("🔍 Check All")
    grid_correct_count = 0

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
                grid_correct_count += 1
                with col4:
                    st.success("✓")
            else:
                st.session_state.streak = 0
                with col4:
                    st.error(f"{correct['Simple Past']}, {correct['Past Participle']}")
                new_reminders = check_reminders(row['Base Form'], sp, pp)
                for reminder in new_reminders:
                    st.warning(f"⚠️ Reminder: {reminder['emoji']} {reminder['name']} - {reminder['description']}")

            new_badges = check_badges(streak=st.session_state.streak)
            for badge in new_badges:
                show_achievement_banner(f"{badge['emoji']} {badge['name']} - {badge['description']}")

    if check_pressed and grid_correct_count == 10:
        new_badges = check_badges(trigger_name="grid_perfect")
        for badge in new_badges:
            show_achievement_banner(f"{badge['emoji']} {badge['name']} - {badge['description']}")
        
        # Set a flag to clear inputs on next rerun instead of immediate clearing
        st.session_state["reset_grid"] = True

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

elif mode == "Single Verb Quiz":
    st.header("🎯 Single Verb Quiz")

    def check_answer_callback():
        is_correct, correct = check_answers(
            st.session_state.current_verb['Base Form'],
            st.session_state.user_sp,
            st.session_state.user_pp
        )
        st.session_state.attempts += 1

        if is_correct:
            st.session_state.score += 1
            st.session_state.streak += 1
            st.session_state.feedback = ("success", "Correct! ✅")
        else:
            st.session_state.streak = 0
            correct_text = f"Incorrect. Correct answers: {correct['Simple Past']}, {correct['Past Participle']}"
            st.session_state.feedback = ("error", correct_text)

            # Add mistake to mistake list (like in grid mode)
            st.session_state.mistakes.append({
                "base_form": st.session_state.current_verb['Base Form'],
                "simple_past": st.session_state.user_sp,
                "past_participle": st.session_state.user_pp
            })

            # Check reminders for the mistake, show warnings if any
            new_reminders = check_reminders(
                st.session_state.current_verb['Base Form'],
                st.session_state.user_sp,
                st.session_state.user_pp
            )
            for reminder in new_reminders:
                st.warning(f"⚠️ Reminder: {reminder['emoji']} {reminder['name']} - {reminder['description']}")

        # Check badges on streak or triggers, show achievement banners
        new_badges = check_badges(streak=st.session_state.streak)
        for badge in new_badges:
            show_achievement_banner(f"{badge['emoji']} {badge['name']} - {badge['description']}")

        st.session_state.user_sp = ""
        st.session_state.user_pp = ""
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    # Then outside the function, the UI input/output:

    if "current_verb" not in st.session_state:
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    if "user_sp" not in st.session_state:
        st.session_state.user_sp = ""
    if "user_pp" not in st.session_state:
        st.session_state.user_pp = ""
    if "feedback" not in st.session_state:
        st.session_state.feedback = ("", "")

    verb = st.session_state.current_verb
    st.write(f"**Base form:** {verb['Base Form']}")

    user_sp = st.text_input("Simple Past", key="user_sp")
    user_pp = st.text_input("Past Participle", key="user_pp")

    if st.button("Check Answer", on_click=check_answer_callback):
        pass

    if st.session_state.feedback[0] == "success":
        st.success(st.session_state.feedback[1])
    elif st.session_state.feedback[0] == "error":
        st.error(st.session_state.feedback[1])

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

    st.header("😬 Reminders: Learn from Your Mistakes")
    reminder_table = []
    for reminder in reminders:
        status = "✅ Earned" if reminder["name"] in st.session_state.reminders else "🔒"
        reminder_table.append([reminder["emoji"], reminder["name"], reminder["description"], status])
    st.table(pd.DataFrame(reminder_table, columns=["Icon", "Reminder Name", "Description", "Status"]))
