import streamlit as st
import pandas as pd
from gtts import gTTS
import os
import base64

# Sample verbs DataFrame (replace with your actual data)
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

# Function to generate audio and return HTML player
def text_to_audio_html(text, filename):
    tts = gTTS(text)
    tts.save(filename)
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    return audio_html

# Initialize session state
if 'load_new_verb' not in st.session_state:
    st.session_state.load_new_verb = True

if 'current_verb' not in st.session_state:
    st.session_state.current_verb = verbs_df.sample(1).iloc[0]

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# App mode
mode = "Single Verb Quiz"

if mode == "Single Verb Quiz":
    st.title("Single Verb Quiz")

    if st.session_state.load_new_verb:
        st.session_state.current_verb = verbs_df.sample(1).iloc[0]
        st.session_state.load_new_verb = False

    verb = st.session_state.current_verb

    st.markdown(f"### Base Form: **{verb['Base Form']}**")
    st.markdown(text_to_audio_html(verb['Base Form'], "base.mp3"), unsafe_allow_html=True)

    simple_past = st.text_input("Enter the Simple Past form:", key="single_sp")
    past_participle = st.text_input("Enter the Past Participle form:", key="single_pp")

    if st.button("Submit"):
        st.session_state.attempts += 1
        is_correct, correct = check_answers(verb['Base Form'], simple_past, past_participle)
        if is_correct:
            st.session_state.score += 1
            st.success("Correct! Well done!")
        else:
            st.error("Incorrect.")
            st.info(f"Correct forms: Simple Past - {correct['Simple Past']}, Past Participle - {correct['Past Participle']}")
            st.markdown("### Listen to correct forms:")
            st.markdown(text_to_audio_html(correct['Simple Past'], "sp.mp3"), unsafe_allow_html=True)
            st.markdown(text_to_audio_html(correct['Past Participle'], "pp.mp3"), unsafe_allow_html=True)

    if st.button("New Verb"):
        st.session_state.load_new_verb = True
        st.experimental_rerun()

    st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")
