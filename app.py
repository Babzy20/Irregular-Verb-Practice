import streamlit as st
import pandas as pd

# Load verbs from CSV
verbs_df = pd.read_csv('verbs 5.csv')

# Load reminders from CSV
reminders_df = pd.read_csv('reminders.csv')

# Convert reminders DataFrame to dictionary
reminders = reminders_df.to_dict(orient='records')

# Function to get reminder based on trigger
def get_reminder(trigger):
    for reminder in reminders:
        if reminder['trigger'] == trigger:
            return reminder['name'], reminder['emoji'], reminder['description']
    return None, None, None

# Streamlit app code
def main():
    st.title("Irregular Verb Practice App")

mode = st.radio("Choose a mode:", ["Single Verb Quiz", "Grid Mode"], key="mode_selector")

    if mode == "Single Verb Quiz":
        st.header("Single Verb Quiz")
        verb = st.selectbox("Choose a verb", verbs_df['Base Form'])
        correct_simple_past = verbs_df[verbs_df['Base Form'] == verb]['Simple Past'].values[0]
        correct_past_participle = verbs_df[verbs_df['Base Form'] == verb]['Past Participle'].values[0]

        user_simple_past = st.text_input("Simple Past")
        user_past_participle = st.text_input("Past Participle")

        if st.button("Check"):
            if user_simple_past == correct_simple_past and user_past_participle == correct_past_participle:
                st.success("Correct!")
            else:
                st.error("Incorrect!")
                if user_simple_past != correct_simple_past:
                    name, emoji, description = get_reminder('simple_past')
                    if name:
                        st.warning(f"{emoji} {name}: {description}")
                if user_past_participle != correct_past_participle:
                    name, emoji, description = get_reminder('past_participle')
                    if name:
                        st.warning(f"{emoji} {name}: {description}")

    elif mode == "Grid Mode":
        st.header("Grid Mode")
        grid_verbs = verbs_df.sample(10)
        user_inputs = {}
st.write("### Fill in the forms:")
for i, row in grid_verbs.iterrows():
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
    with col1:
        st.markdown(f"**{row["Base Form"]}**")
    with col2:
        simple_past = st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
    with col3:
        past_participle = st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")
    user_inputs[row["Base Form"]] = {
        "simple_past": simple_past,
        "past_participle": past_participle
    }
            user_inputs[row['Base Form']] = {
                'simple_past': st.text_input(f"{row['Base Form']} - Simple Past"),
                'past_participle': st.text_input(f"{row['Base Form']} - Past Participle")
            }

        if st.button("Check All"):
st.write("### Fill in the forms:")
for i, row in grid_verbs.iterrows():
    col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
    with col1:
        st.markdown(f"**{row["Base Form"]}**")
    with col2:
        simple_past = st.text_input("", key=f"sp_{i}", placeholder="Simple Past", label_visibility="collapsed")
    with col3:
        past_participle = st.text_input("", key=f"pp_{i}", placeholder="Past Participle", label_visibility="collapsed")
    user_inputs[row["Base Form"]] = {
        "simple_past": simple_past,
        "past_participle": past_participle
    }
                correct_simple_past = row['Simple Past']
                correct_past_participle = row['Past Participle']
                user_simple_past = user_inputs[row['Base Form']]['simple_past']
                user_past_participle = user_inputs[row['Base Form']]['past_participle']

                if user_simple_past == correct_simple_past and user_past_participle == correct_past_participle:
                    st.success(f"{row['Base Form']}: Correct!")
                else:
                    st.error(f"{row['Base Form']}: Incorrect!")
                    if user_simple_past != correct_simple_past:
                        name, emoji, description = get_reminder('simple_past')
                        if name:
                            st.warning(f"{emoji} {name}: {description}")
                    if user_past_participle != correct_past_participle:
                        name, emoji, description = get_reminder('past_participle')
                        if name:
                            st.warning(f"{emoji} {name}: {description}")

if __name__ == "__main__":
    main()
