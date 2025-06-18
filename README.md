# Conci – AI-Powered Hotel Room Voice Concierge

**Conci** is an open-source MVP of a smart voice concierge designed for hotel rooms. Guests can speak naturally, and Conci understands their intent, categorizes requests, logs them, and notifies staff — all with privacy-first, local browser-based speech recognition.

---

## 🎯 MVP Features

### 🗣️ Guest-Side (`app.py`)
- **Voice to Intent:** Guests interact using their browser mic via the Web Speech API.
- **Smart Categorization:** Requests like towels, dining, or emergencies are auto-tagged.
- **Real-Time Logging:** Each interaction is stored with a timestamp, room number, and guest name.
- **Local + Private:** All recognition happens in-browser (no external APIs).

### 👨‍💼 Staff-Side (`staffdashboard.py`)
- **Live Intent Feed:** Staff see a live, color-coded dashboard of service requests.
- **Auto Categorization:** Requests are grouped (Housekeeping, F&B, Engineering, Emergency).
- **Sentiment Simulation:** Randomized sentiment tagging to simulate urgency.
- **Status Tracking:** Staff can update task statuses (New, In Progress, Done).
- **Revenue Dashboard:** Displays sample upsell and RevPAR metrics.
- **Bulk Admin Tools:** Push wake-word changes or promos to all rooms.

---

## 🛠️ Tech Stack

- **Streamlit** – UI, logic, and session state handling
- **Web Speech API (HTML/JS)** – Voice recognition in the browser
- **Python** – Backend logic
- **Pandas** – Table rendering and formatting
- **Bokeh** – Micro-interactions (voice trigger button)

---

## 🚀 Run Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/conci-voice-concierge.git
   cd conci-voice-concierge
2. **Install dependencies:**
    ```bash
   pip install numpy==1.23.5 bokeh==2.4.3 streamlit==1.30 streamlit-bokeh-events
3. **Run the app:**
    ```bash
   streamlit run app.py

### Note:

**Use Google Chrome (Web Speech API only works in Chrome).**

**This MVP uses st.session_state for all logic — ideal for testing, not multi-user production.**


### Author
Dhiya C Jayakumar
AI Engineer | Open Source Builder
dhiya.cjayakumar@gmail.com
www.linkedin.com/in/dhiya-cjayakumar
