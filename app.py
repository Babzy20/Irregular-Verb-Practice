import streamlit as st
import pandas as pd

# Load the list of irregular verbs
verbs_df = pd.read_csv('verbs.csv')

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
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

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
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

elif mode == "Grid Mode":
    st.header("Grid Mode")
    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

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
            if is_correct:
                st.success(f"{base_form}: Correct!")
            else:
                st.error(f"{base_form}: Incorrect. Correct: {correct['Simple Past']}, {correct['Past Participle']}")
