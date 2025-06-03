import streamlit as st
import pandas as pd

# Load the full list of verbs from CSV
@st.cache_data
def load_verbs():
    return pd.read_csv("irregular_verbs.csv")

verbs_df = load_verbs()

# Function to check answers
def check_answers(base, sp, pp):
    row = verbs_df[verbs_df["Base Form"] == base].iloc[0]
    correct = {
        "Simple Past": row["Simple Past"],
        "Past Participle": row["Past Participle"]
    }
    is_correct = (sp.strip().lower() == correct["Simple Past"].lower() and
                  pp.strip().lower() == correct["Past Participle"].lower())
    return is_correct, correct

# Initialize session state
if 'load_new_verb' not in st.session_state:
    st.session_state.load_new_verb = True

if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# App title
st.title("Single Verb Quiz")

# Load a new verb if needed
if st.session_state.load_new_verb:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]
    st.session_state.load_new_verb = False

verb = st.session_state.current_verb

# Display the base form
st.markdown(f"### Base Form: **{verb['Base Form']}**")

# Input fields
simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")

# Submit button
if st.button("Submit"):
    st.session_state.attempts += 1
    is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
    if is_correct:
        st.session_state.score += 1
        st.success("Correct! Well done!")
    else:
        st.error("Incorrect.")
        st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")

# New verb button
if st.button("New Verb"):
    st.session_state.load_new_verb = True

# Score display
st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")
import streamlit as st
import pandas as pd

# Sample verbs DataFrame (replace with your full dataset)
verbs_df = pd.DataFrame([
    {"Base Form": "go", "Simple Past": "went", "Past Participle": "gone"},
    {"Base Form": "eat", "Simple Past": "ate", "Past Participle": "eaten"},
    {"Base Form": "write", "Simple Past": "wrote", "Past Participle": "written"},
])

# Function to check answers
def check_answers(base, sp, pp):
    row = verbs_df[verbs_df["Base Form"] == base].iloc[0]
    correct = {
        "Simple Past": row["Simple Past"],
        "Past Participle": row["Past Participle"]
    }
    is_correct = (sp.strip().lower() == correct["Simple Past"].lower() and
                  pp.strip().lower() == correct["Past Participle"].lower())
    return is_correct, correct

# Initialize session state
if 'load_new_verb' not in st.session_state:
    st.session_state.load_new_verb = True

if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# App title
st.title("Single Verb Quiz")

# Load a new verb if needed
if st.session_state.load_new_verb:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]
    st.session_state.load_new_verb = False

verb = st.session_state.current_verb

# Display the base form
st.markdown(f"### Base Form: **{verb['Base Form']}**")

# Input fields
simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")

# Submit button
if st.button("Submit"):
    st.session_state.attempts += 1
    is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
    if is_correct:
        st.session_state.score += 1
        st.success("Correct! Well done!")
    else:
        st.error("Incorrect.")
        st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")

# New verb button
if st.button("New Verb"):
    st.session_state.load_new_verb = True

# Score display
st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")
