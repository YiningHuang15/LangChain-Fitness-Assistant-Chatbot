import streamlit as st
from lc import FITNESS_ASSISTANT_GRAPH, FitnessAgentState

st.set_page_config(page_title="💪 AI Fitness Chatbot", page_icon="🤖", layout="centered")

st.title("💬 AI Fitness Chatbot")
# Bigger caption using HTML
st.markdown('<p style="font-size:20px; color:gray;">Plan smarter. Play together.</p>', unsafe_allow_html=True)

# ---- Initialize chat history ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---- Display chat history ----
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- User Input ----
if user_input := st.chat_input("Ask me about workouts, events, or anything fitness-related..."):
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Run the LangGraph pipeline
                initial_state: FitnessAgentState = {
                    "user_input": user_input,
                    "intent": None,
                    "exercise_plan": None,
                    "matched_event": None,
                    "booking_confirmation": None,
                    "assistant_reply": None
                }
                final_state = FITNESS_ASSISTANT_GRAPH.invoke(initial_state)
                
                 # ✅ Save matched_event to Streamlit session state (even if not booked)
                if final_state.get("matched_event"):
                    st.session_state["matched_event"] = final_state["matched_event"]

                # Build assistant message based on output
                if final_state.get("assistant_reply"):
                    response = final_state["assistant_reply"]

                elif final_state.get("exercise_plan"):
                    plan = final_state["exercise_plan"]
                    response = f"### {plan.title}\n"
                    for i, ex in enumerate(plan.exercises, start=1):
                        response += f"**{i}. {ex.exercise}** — {ex.setsxreps} ({ex.focus})\n{ex.notes}\n\n"
                    st.session_state["latest_workout"] = plan

                elif final_state.get("booking_confirmation"):
                    response = f"✅ {final_state['booking_confirmation']}"
                    st.session_state["latest_event"] = final_state.get("matched_event")

                else:
                    response = "🤔 I’m not sure how to help with that yet — try asking in another way!"

            except Exception as e:
                response = f"⚠️ Something went wrong: {e}"

            st.markdown(response)

    # Save assistant message
    st.session_state["messages"].append({"role": "assistant", "content": response})
