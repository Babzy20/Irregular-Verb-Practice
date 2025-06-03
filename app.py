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

# Initialize session state variables
if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# Custom styles for buttons
custom_button_styles = """
<style>
#new-verb-button button {
    background-color: #e74c3c !important;
    color: white !important;
    font-weight: bold;
}
#submit-button button {
    background-color: #27ae60 !important;
    color: white !important;
    font-weight: bold;
}
#new-verbs-button button {
    background-color: #2980b9 !important;
    color: white !important;
    font-weight: bold;
}
#reset-score-button button {
    background-color: #7f8c8d !important;
    color: white !important;
    font-weight: bold;
}
</style>
"""
st.markdown(custom_button_styles, unsafe_allow_html=True)

# App title
st.title("Irregular Verbs Practice")

# Mode selection
mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

if mode == "Single Verb Quiz":
    st.header("Single Verb Quiz")

    st.markdown('<div id="new-verb-button">', unsafe_allow_html=True)
    new_verb_clicked = st.button("New Verb", key="new_verb_button")
    st.markdown('</div>', unsafe_allow_html=True)

    if new_verb_clicked:
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]

    verb = st.session_state.current_verb
    st.write(f"Base Form: **{verb['Base Form']}**")

    simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
    past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")

    st.markdown('<div id="submit-button">', unsafe_allow_html=True)
    submit_clicked = st.button("Submit", key="submit_button")
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_clicked:
        st.session_state.attempts += 1
        is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
        if is_correct:
            st.session_state.score += 1
            st.success("Correct! Well done!")
        else:
            st.error("Incorrect.")
            st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

elif mode == "Grid Mode":
    st.header("Grid Mode")
    if "grid_verbs" not in st.session_state:
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)

    user_inputs = []
    show_answers = st.button("Check All")

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

    st.markdown('<div id="new-verbs-button">', unsafe_allow_html=True)
    if st.button("New Verbs"):
        st.session_state.grid_verbs = verbs_df.sample(20).reset_index(drop=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write(f"Score: {st.session_state.score}/{st.session_state.attempts}")
    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"Accuracy: {accuracy:.2f}%")

st.markdown('<div id="reset-score-button">', unsafe_allow_html=True)
if st.button("Reset Score"):
    st.session_state.score = 0
    st.session_state.attempts = 0
st.markdown('</div>', unsafe_allow_html=True)
