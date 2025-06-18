import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="Staff Dashboard", layout="wide")
st.title("🛠️ Conci Staff Dashboard")

# --- Ensure the service log is initialized ---
if "service_log" not in st.session_state:
    st.session_state.service_log = []

# --- Category inference logic ---
def categorize_response(response):
    response = response.lower()
    if any(word in response for word in ["towel", "toothbrush", "luggage", "water", "housekeeping"]):
        return "Housekeeping"
    elif any(word in response for word in ["food", "spa", "dining", "restaurant", "cuisine", "drinks"]):
        return "F&B"
    elif any(word in response for word in ["emergency", "help", "fire", "glass break", "co2", "smoke"]):
        return "Emergency"
    elif any(word in response for word in ["engineering", "not working", "broken"]):
        return "Engineering"
    else:
        return "General"

# --- Enrich log entries with category, status, ticket, sentiment ---
for entry in st.session_state.service_log:
    if "Category" not in entry:
        entry["Category"] = categorize_response(entry["Response"])
    if "Status" not in entry:
        entry["Status"] = "New"
    if "Ticket Sent" not in entry:
        entry["Ticket Sent"] = "Yes"
    if "Sentiment" not in entry:
        entry["Sentiment"] = random.choice(["Positive", "Neutral", "Urgent"])

# --- Build DataFrame for display ---
df = pd.DataFrame(st.session_state.service_log)

# --- Color mapping for categories --- yellow, green, blue, red, grey respectively.
category_colors = {
    "Housekeeping": "#ffeb3b",
    "F&B": "#8bc34a",
    "Engineering": "#03a9f4",
    "Emergency": "#f44336", 
    "General": "#e0e0e0"  }

# --- Live Intent Feed ---
st.markdown("### 🔔 Live Intent Feed")
if not df.empty:
    for i, entry in df.iterrows():
        color = category_colors.get(entry["Category"], "#ffffff")
        with st.container():
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; border-left: 8px solid {color}; padding: 10px; margin-bottom: 10px;">
                    <strong>Time:</strong> {entry['Time']}<br>
                    <strong>Room:</strong> {entry['Room']}<br>
                    <strong>Guest:</strong> {entry.get('Guest', 'Unknown')}<br>
                    <strong>Command:</strong> {entry['Command']}<br>
                    <strong>Response:</strong> {entry['Response']}<br>
                    <strong>Category:</strong> {entry['Category']}<br>
                    <strong>Ticket Sent:</strong> {entry['Ticket Sent']}<br>
                    <strong>Sentiment:</strong> {entry['Sentiment']}<br>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Editable status
            new_status = st.selectbox(
                f"Status for Room {entry['Room']} - {entry['Command'][:20]}",
                options=["New", "In Progress", "Done"],
                index=["New", "In Progress", "Done"].index(entry["Status"]),
                key=f"status_{i}"
            )
            st.session_state.service_log[i]["Status"] = new_status
else:
    st.info("No service requests yet.")

# --- Revenue Dashboard ---
st.header("💰 Revenue Dashboard")
st.metric("Upsell Conversions", random.randint(10, 20))
st.metric("Incremental RevPAR", f"${random.randint(30, 60)}")

# --- Bulk Room Admin ---
st.header("🛎️ Bulk Room Admin")
promo = st.text_input("Push new wake-word or promo to rooms:", key="promo_input")
if st.button("Push Promo"):
    st.session_state.current_promo = promo  # Save promo to session state
    st.success(f"Promo '{promo}' pushed to all devices!")
