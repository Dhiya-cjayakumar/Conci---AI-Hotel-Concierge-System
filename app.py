import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from bokeh.layouts import column
from streamlit_bokeh_events import streamlit_bokeh_events
from datetime import datetime
import re

st.set_page_config(page_title="Conci Guest Interface", layout="centered")
st.title("🎤 Conci: Hotel Voice Concierge")

# --- Custom CSS for result/command area ---
st.markdown("""
    <style>
    .voice-box {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        border-radius: 18px;
        padding: 32px 24px;
        margin-top: 18px;
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .voice-box-text {
        color: #fff;
        font-size: 1.2rem;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        text-align: center;
        letter-spacing: 0.02em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Show Promo Message if Available ---
if "current_promo" in st.session_state and st.session_state.current_promo:
    st.info(f"📢 Promo: {st.session_state.current_promo}")

# --- Session State Initialization ---
if "service_log" not in st.session_state:
    st.session_state.service_log = []

if "last_logged_command" not in st.session_state:
    st.session_state.last_logged_command = None

if "guest_profile" not in st.session_state:
    st.session_state.guest_profile = {
        "name": "Alex",
        "tier": "Silver",
        "late_checkout": True
    }

st.sidebar.header("Guest Profile")
guest_name = st.sidebar.text_input("Name", value=st.session_state.guest_profile.get("name", "Alex"), key="guest_name")
loyalty_tier = st.sidebar.selectbox("Loyalty Tier", ["Silver", "Gold", "Platinum"], index=["Silver", "Gold", "Platinum"].index(st.session_state.guest_profile.get("tier", "Silver")), key="loyalty_tier")
late_checkout = st.sidebar.checkbox("Late Checkout Eligible", value=st.session_state.guest_profile.get("late_checkout", True), key="late_checkout")
st.session_state.guest_profile = {
    "name": guest_name,
    "tier": loyalty_tier,
    "late_checkout": late_checkout
}

if "room_state" not in st.session_state:
    st.session_state.room_state = {
        "lights": True,
        "blinds": False,
        "thermostat": 22,
        "tv_input": "HDMI1"
    }

st.sidebar.header("Room Controls")
lights = st.sidebar.toggle("Lights", value=st.session_state.room_state["lights"])
blinds = st.sidebar.toggle("Blinds", value=st.session_state.room_state["blinds"])
thermostat = st.sidebar.slider("Thermostat (°C)", 16, 30, st.session_state.room_state["thermostat"])
tv_input = st.sidebar.selectbox("TV Input", ["HDMI1", "HDMI2", "Netflix", "YouTube"], index=["HDMI1", "HDMI2", "Netflix", "YouTube"].index(st.session_state.room_state["tv_input"]))
st.session_state.room_state = {
    "lights": lights, "blinds": blinds, "thermostat": thermostat, "tv_input": tv_input
}

st.sidebar.header("Privacy & Safety")
mic_enabled = st.sidebar.toggle("Mic Enabled", value=True)
if not mic_enabled:
    st.warning("Microphone is OFF for privacy.")
device_only_mode = st.sidebar.toggle("Device-Only Voice Mode", value=False)

# --- Intent Detection Logic ---
def detect_intent_and_room(command):
    command = command.lower()
    room_match = re.search(r"room\s*(\d+)", command)
    room_number = room_match.group(1) if room_match else "unknown"

    # Lights control
    if "turn off the lights" in command or "lights off" in command:
        st.session_state.room_state["lights"] = False
        return room_number, f"Lights turned off for room {room_number}"
    if "turn on the lights" in command or "lights on" in command:
        st.session_state.room_state["lights"] = True
        return room_number, f"Lights turned on for room {room_number}"

    # Blinds control
    if "open the blinds" in command or "blinds up" in command:
        st.session_state.room_state["blinds"] = True
        return room_number, f"Blinds opened for room {room_number}"
    if "close the blinds" in command or "blinds down" in command:
        st.session_state.room_state["blinds"] = False
        return room_number, f"Blinds closed for room {room_number}"

    # Thermostat control
    if "set thermostat to" in command or "temperature" in command:
        temp_match = re.search(r"set thermostat to (\d+)", command)
        if temp_match:
            temp = int(temp_match.group(1))
            st.session_state.room_state["thermostat"] = temp
            return room_number, f"Thermostat set to {temp}°C for room {room_number}"
        return room_number, f"Thermostat adjustment will be done shortly for room {room_number}"

    # TV input control
    for option in ["HDMI1", "HDMI2", "Netflix", "YouTube"]:
        if f"set tv to {option.lower()}" in command or f"switch tv to {option.lower()}" in command:
            st.session_state.room_state["tv_input"] = option
            return room_number, f"TV input set to {option} for room {room_number}"

    # Existing intents...
    if "towel" in command or "tissue" in command:
        return room_number, f"Requesting fresh towels to room {room_number}"
    elif "toothbrush" in command:
        return room_number, f"Delivering toothbrush to room {room_number}"
    elif "menu" in command:
        return room_number, f"Showing today's menu for room {room_number}"
    elif "water" in command or "thirsty" in command:
        return room_number, f"Delivering water bottles to room {room_number}"
    elif "luggage" in command:
        return room_number, f"Luggage pickup requested from room {room_number}"
    elif "not working" in command or "fix" in command:
        return room_number, f"Engineering work requested from room {room_number}"
    elif "food" in command or "order" in command or "hungry" in command:
        return room_number, f"Sending food to room {room_number}"
    elif "emergency" in command or "help" in command or "fire" in command or "glass break" in command or "co2" in command or "smoke" in command:
        return room_number, f"Emergency alert triggered for room {room_number}"
    else:
        return room_number, f"Your request is being addressed for room {room_number}"

# --- Voice Input Interface ---
st.markdown("Click the button and speak. Your recognized voice command will appear below.")
if mic_enabled:
    stt_button = Button(label="🎤 Click to Speak", width=695, height=110, button_type="success")
    stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    recognition.onresult = function(event) {
        var value = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                value += event.results[i][0].transcript;
            }
        }
        if (value !== '') {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    };
    recognition.start();
    """))

    bokeh_layout = column(stt_button, sizing_mode="fixed")
    result = streamlit_bokeh_events(
        bokeh_layout,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=120,
        debounce_time=0
    )
else:
    result = None

# --- Recognized Command/Result Display (Styled) ---
if result and "GET_TEXT" in result:
    st.markdown(f"""
        <div class="voice-box">
            <span class="voice-box-text">
                <b>Recognized:</b> {result['GET_TEXT']}
            </span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="voice-box">
            <span class="voice-box-text">
                🎤 Your recognized voice command will appear here.
            </span>
        </div>
    """, unsafe_allow_html=True)

   








def assign_department_and_ticket(response):
    response = response.lower()
    now = datetime.now().strftime('%H%M%S')
    if any(word in response for word in ["towel", "toothbrush", "luggage", "water"]):
        return "Housekeeping", f"HSK-{now}"
    elif any(word in response for word in ["food", "spa", "dining", "restaurant", "cuisine", "dessert", "menu", "order"]):
        return "F&B", f"FNB-{now}"
    elif any(word in response for word in ["emergency", "help", "fire", "glass break", "co2", "smoke"]):
        return "Emergency", f"EMG-{now}"
    elif any(word in response for word in ["engineering", "not working", "fix"]):
        return "Engineering", f"ENG-{now}"
    else:
        return "General", f"GEN-{now}"

def get_sentiment(command):
    negative_words = ["angry", "upset", "bad", "terrible", "not happy", "disappointed", "unacceptable", "horrible", "worst", "complaint"]
    positive_words = ["thank you", "great", "awesome", "good", "happy", "excellent", "love", "perfect", "amazing", "thankyou"]
    command_lower = command.lower()
    if any(word in command_lower for word in negative_words):
        return "Negative"
    elif any(word in command_lower for word in positive_words):
        return "Positive"
    else:
        return "Neutral"

# --- Result Processing ---
if result and "GET_TEXT" in result:
    command = result["GET_TEXT"]
    profile = st.session_state.guest_profile

    # Show menu image if guest asks for menu/order/food
    if any(word in command.lower() for word in ["menu", "want to order", "food"]):
        st.image(
            "https://blog.photoadking.com/wp-content/uploads/2023/03/image-158-791x1024.png",
            caption="Room Service Menu",
            use_column_width=True
        )

    room_number, response = detect_intent_and_room(command)
    sentiment = get_sentiment(command)
    unresolved = "being addressed" in response.lower()  # True if fallback

    st.markdown(
        f"🧠 **Conci's Response:** {response} <br>_Guest: {profile['name']} ({profile['tier']})_",
        unsafe_allow_html=True
    )
    




    # Only log new commands if not in device-only mode
    if not device_only_mode:
        if command != st.session_state.last_logged_command:
            department, ticket_id = assign_department_and_ticket(response)
            st.session_state.service_log.append({
                "Time": datetime.now().strftime("%I:%M:%S %p"),
                "Room": room_number,
                "Command": command,
                "Response": response,
                "Guest": profile["name"],
                "Sentiment": sentiment,
                "Unresolved": unresolved,
                "Department": department,
                "Ticket ID": ticket_id
            })
            st.session_state.last_logged_command = command

            # Alert GM if negative sentiment AND unresolved
            if sentiment == "Negative" and unresolved:
                st.error("🚨 GM Alert: Negative sentiment and unresolved request detected!")
    else:
        st.info("Device-Only Mode: This command was processed locally and not logged.")

else:
    st.info("Awaiting your voice command...")

st.markdown("### 🏠 Current Room State")
room_state = st.session_state.room_state
st.write(f"**Lights:** {'On' if room_state['lights'] else 'Off'}")
st.write(f"**Blinds:** {'Open' if room_state['blinds'] else 'Closed'}")
st.write(f"**Thermostat:** {room_state['thermostat']}°C")
st.write(f"**TV Input:** {room_state['tv_input']}")


# --- Dining & Spa Booking ---
st.header("🍽️ Dining & Spa Booking")
if st.button("Book Table at Restaurant"):
    st.success("Table booked! Enjoy your meal.")
    st.session_state.service_log.append({
        "Time": datetime.now().strftime("%I:%M:%S %p"),
        "Room": "unknown",
        "Command": "Book Table",
        "Response": "Table booked at restaurant",
        "Guest": st.session_state.guest_profile["name"],
        "Sentiment": "Neutral",
        "Unresolved": False,
        "Department": "F&B",
        "Ticket ID": f"FNB-{datetime.now().strftime('%H%M%S')}"
    })
if st.button("Book Spa Appointment"):
    st.success("Spa appointment booked!")
    st.session_state.service_log.append({
        "Time": datetime.now().strftime("%I:%M:%S %p"),
        "Room": "unknown",
        "Command": "Book Spa",
        "Response": "Spa appointment booked",
        "Guest": st.session_state.guest_profile["name"],
        "Sentiment": "Neutral",
        "Unresolved": False,
        "Department": "F&B",
        "Ticket ID": f"FNB-{datetime.now().strftime('%H%M%S')}"
    })

# --- Local Recommendations ---
st.header("🌆 Local Recommendations")
if st.button("Show Jogging Routes"):
    st.info("Try the Riverside Park loop (3km) or City Center circuit (5km).")
if st.button("Book a Ride"):
    st.success("Ride booked! Car will arrive in 5 minutes.")

# --- Log Preview for Guest ---
if st.session_state.service_log:
    st.markdown("---")
    st.subheader("📋 Service Request Log (Preview)")
    st.dataframe(st.session_state.service_log, use_container_width=True)

import pandas as pd
import numpy as np

if st.session_state.service_log:
    df = pd.DataFrame(st.session_state.service_log)
    if "Room" in df and "Sentiment" in df:
        st.markdown("#### 🗺️ Sentiment Heatmap (by Room)")
        heatmap_data = df.groupby(['Room', 'Sentiment']).size().unstack(fill_value=0)
        st.dataframe(heatmap_data)
