import streamlit as st

st.set_page_config(page_title="💪 Exercise Plan", page_icon="💪", layout="centered")

st.title("🏋️ Your Latest Exercise Plan")

if "latest_workout" not in st.session_state or st.session_state["latest_workout"] is None:
    st.info("No exercise plan yet. Go back to the **AI Fitness Chatbot** page to generate one!")
else:
    plan = st.session_state["latest_workout"]
    st.subheader(plan.title)

    st.write("---")

    # Ensure session_state for completed exercises
    if "completed_exercises" not in st.session_state:
        st.session_state.completed_exercises = [False] * len(plan.exercises)

    for i, ex in enumerate(plan.exercises, start=1):
        # Use a card-like container for each exercise
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 1rem 1.2rem;
                    margin-bottom: 0.8rem;
                    border-radius: 0.8rem;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
                ">
                    <h4 style="margin-bottom: 0.3rem;">{i}. {ex.exercise}</h4>
                    <p style="margin: 0.2rem 0;">🦾 <b>{ex.setsxreps}</b> &nbsp;|&nbsp; 🎯 {ex.focus}</p>
                    <p style="font-size: 0.9rem; color: #555;">💬 {ex.notes}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Checkbox to mark completion
            st.session_state.completed_exercises[i - 1] = st.checkbox(
                f"✅ Mark as completed",
                key=f"exercise_{i}",
                value=st.session_state.completed_exercises[i - 1],
            )

    st.write("---")
    completed_count = sum(st.session_state.completed_exercises)
    total_count = len(plan.exercises)
    st.success(f"Progress: {completed_count}/{total_count} exercises completed 💪")
