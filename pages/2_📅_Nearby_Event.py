import streamlit as st
import pandas as pd

st.set_page_config(page_title="Your Latest Nearby Events", layout="wide")
st.title("📅 Nearby Events")

# ---- Fetch matched events from session_state ----
matched_events = st.session_state.get("latest_event") or st.session_state.get("matched_event")

if not matched_events:
    st.warning("No nearby events yet. Go back to the **AI Fitness Chatbot** to search for events!")
    st.stop()

# ---- Convert to DataFrame ----
df = pd.DataFrame(matched_events)

# ---- Add Status column: first event booked ----
df["Status"] = ["✅ Booked" if i == 0 else "" for i in range(len(df))]

# ---- Rearrange columns for better display ----
columns_order = ["Status", "game_type", "game_date", "game_time", "game_location", "game_level"]
df = df[columns_order]

# ---- Display dataframe with styling ----
st.dataframe(
    df.style.set_properties(**{
        "text-align": "left",
        "font-size": "14px"
    }).set_table_styles([
        {"selector": "th", "props": [("text-align", "left"), ("background-color", "#f0f0f0"), ("font-weight", "bold")]},
        {"selector": "td", "props": [("padding", "8px")]}
    ]),
    height=300
)

# ---- Display booking confirmation ----
booked_event = matched_events[0]
confirmation_msg = (
    f"✅ Your {booked_event['game_type']} event on {booked_event['game_date']} "
    f"at {booked_event['game_time']} in {booked_event['game_location']} is booked!"
)
st.success(confirmation_msg)