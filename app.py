import streamlit as st
import pandas as pd
import random

# Load the list of irregular verbs
verbs_df = pd.read_csv('verbs.csv')

# Function to check answers
def check_answers(base_form, simple_past, past_participle):
    correct = verbs_df[verbs_df['Base Form'] == base_form].iloc[0]
    return (
        simple_past.strip().lower() == correct['Simple Past'].strip().lower() and
        past_participle.strip().lower() == correct['Past Participle'].strip().lower()
    ), correct

# Initialize session state variables
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "current_verb" not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]
if "grid_verbs" not in st.session_state:
    st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

# App title
st.title("Irregular Verbs Practice for ESL Students")

# Display score
st.write(f"Score: {st.session_state.score} / {st.session_state.attempts}")

# Mode selection
mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

if mode == "Single Verb Quiz":
    st.header("Single Verb Quiz")

    verb = st.session_state.current_verb
    st.write(f"Base Form: **{verb['Base Form']}**")

    simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
    past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")

    if st.button("Submit"):
        is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
        st.session_state.attempts += 1
        if is_correct:
            st.session_state.score += 1
            st.success("Correct! Well done!")
        else:
            st.error("Incorrect.")
            st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")
        # Refresh for next round
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    if st.button("New Verb"):
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

elif mode == "Grid Mode":
    st.header("Grid Mode")

    user_inputs = []
    st.write("### Fill in the forms:")
    for i, row in st.session_state.grid_verbs.iterrows():
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        with col1:
            st.markdown(f"**{row['Base Form']}**")
        with col2:
            simple_past = st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
        with col3:
            past_participle = st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")
        user_inputs.append((row['Base Form'], simple_past, past_participle))

    if st.button("Check All"):
        for base_form, sp, pp in user_inputs:
            is_correct, correct = check_answers(base_form, sp, pp)
            st.session_state.attempts += 1
            if is_correct:
                st.session_state.score += 1
                st.success(f"{base_form}: Correct!")
            else:
                st.error(f"{base_form}: Incorrect. Correct: {correct['Simple Past']}, {correct['Past Participle']}")

    if st.button("New Verbs"):
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

# Display final score
st.write(f"Final Score: {st.session_state.score} / {st.session_state.attempts}")
