import streamlit as st
import pandas as pd

# Load verbs data
verbs = pd.read_csv('verbs.csv')

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# Function to check answers
def check_answers(base_form, simple_past, past_participle):
    correct = verbs[verbs['Base Form'] == base_form].iloc[0]
    return (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    )

# App title
st.title("📚 Irregular Verbs Practice")

# Mode selection
mode = st.selectbox("Choose Mode", ["Single Verb Mode", "Grid Mode"])

if mode == "Single Verb Mode":
    st.header("🎯 Single Verb Mode")
    verb = verbs.sample(1).iloc[0]
    st.write(f"Base Form: **{verb['Base Form']}**")
    simple_past = st.text_input("Simple Past")
    past_participle = st.text_input("Past Participle")

    if st.button("Check Answer"):
        st.session_state.attempts += 1
        if check_answers(verb['Base Form'], simple_past, past_participle):
            st.session_state.score += 1
            st.success("Correct!")
        else:
            st.error(f"Incorrect! Correct: {verb['Simple Past']}, {verb['Past Participle']}")

elif mode == "Grid Mode":
    st.header("🧩 Grid Mode")

    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs.sample(10).reset_index(drop=True)

    st.write("### Fill in the forms:")
    for i, row in st.session_state.grid_verbs.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
        with col1:
            st.markdown(f"**{row['Base Form']}**")
        with col2:
            st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
        with col3:
            st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")

    if st.button("🔍 Check All"):
        for i, row in st.session_state.grid_verbs.iterrows():
            sp = st.session_state[f"sp_{i}"]
            pp = st.session_state[f"pp_{i}"]
            st.session_state.attempts += 1
            if check_answers(row['Base Form'], sp, pp):
                st.session_state.score += 1
                st.success(f"{row['Base Form']}: ✓")
            else:
                correct = verbs[verbs['Base Form'] == row['Base Form']].iloc[0]
                st.error(f"{row['Base Form']}: {correct['Simple Past']}, {correct['Past Participle']}")

    if st.button("🆕 New Verbs"):
        st.session_state.grid_verbs = verbs.sample(10).reset_index(drop=True)

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")
