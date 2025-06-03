import streamlit as st
import pandas as pd

# Load the list of irregular verbs from the CSV file
verbs_df = pd.read_csv('verbs.csv')

# Function to check the user's answers
def check_answers(base_form, simple_past, past_participle):
    correct_simple_past = verbs_df.loc[verbs_df['Base Form'] == base_form, 'Simple Past'].values[0]
    correct_past_participle = verbs_df.loc[verbs_df['Base Form'] == base_form, 'Past Participle'].values[0]
    
    simple_past_correct = simple_past.lower() == correct_simple_past.lower()
    past_participle_correct = past_participle.lower() == correct_past_participle.lower()
    
    return simple_past_correct, past_participle_correct, correct_simple_past, correct_past_participle

# Streamlit app layout
st.title("ESL Irregular Verbs Practice")

# Select a verb to practice
base_form = st.selectbox("Choose a verb to practice:", verbs_df['Base Form'])

# User input for simple past and past participle
simple_past = st.text_input("Enter the Simple Past form:")
past_participle = st.text_input("Enter the Past Participle form:")

# Check answers when the user submits
if st.button("Submit"):
    simple_past_correct, past_participle_correct, correct_simple_past, correct_past_participle = check_answers(base_form, simple_past, past_participle)
    
    if simple_past_correct and past_participle_correct:
        st.success("Correct! Well done!")
    else:
        st.error("Incorrect. Try again.")
        st.write(f"The correct forms are: Simple Past - {correct_simple_past}, Past Participle - {correct_past_participle}")


