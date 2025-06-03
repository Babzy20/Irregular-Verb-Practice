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

# App title
st.title("Irregular Verbs Practice for ESL Students")

# Mode selection
mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"])

if mode == "Single Verb Quiz":
    st.header("Single Verb Quiz")
    if "current_verb" not in st.session_state:
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    verb = st.session_state.current_verb
    st.write(f"Base Form: **{verb['Base Form']}**")

    simple_past = st.text_input("Enter the Simple Past form:")
    past_participle = st.text_input("Enter the Past Participle form:")

    if st.button("Submit"):
        is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
        if is_correct:
            st.success("Correct! Well done!")
        else:
            st.error("Incorrect.")
            st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")
        # Refresh for next round
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

elif mode == "Grid Mode":
    st.header("Grid Mode")
    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

    user_inputs = []
    for i, row in st.session_state.grid_verbs.iterrows():
        st.write(f"**{row['Base Form']}**")
        col1, col2 = st.columns(2)
        with col1:
            simple_past = st.text_input(f"Simple Past {i+1}", key=f"sp_{i}")
        with col2:
            past_participle = st.text_input(f"Past Participle {i+1}", key=f"pp_{i}")
        user_inputs.append((row['Base Form'], simple_past, past_participle))

    if st.button("Check All"):
        for base_form, sp, pp in user_inputs:
            is_correct, correct = check_answers(base_form, sp, pp)
            if is_correct:
                st.success(f"{base_form}: Correct!")
            else:
                st.error(f"{base_form}: Incorrect. Correct: {correct['Simple Past']}, {correct['Past Participle']}")
