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
