Conci – AI-Powered Hotel Room Voice Concierge

Conci is an open-source MVP of an intelligent voice concierge designed for hotel rooms. It listens to guest commands, understands intent, routes service requests to hotel staff, and logs interactions for efficient operations — all with privacy-first, local browser-based speech recognition.

🎯 MVP Features
🗣️ Guest-Side (app.py)
Voice to Intent: Guests speak naturally via browser mic using Web Speech API.
Smart Recognition: Commands are parsed and categorized (e.g., Housekeeping, F&B, Emergency).
Real-Time Logging: Every request is timestamped and stored in session state.
Context Capture: Room number and guest name logged for every interaction.

👨‍💼 Staff-Side (staffdashboard.py)
Live Intent Feed: Service requests appear in a color-coded dashboard.
Category Highlighting: Requests are auto-categorized (Housekeeping, F&B, Engineering, Emergency).
Sentiment Tagging: Random sentiment scores (MVP simulation).
Editable Statuses: Staff can update status per request (New, In Progress, Done).
Revenue Dashboard: Simulated metrics for RevPAR and upsells.
Bulk Room Admin: Push promos/wake-words across rooms.

🛠️ Tech Stack
Streamlit – frontend + session state
HTML/JS – Web Speech API for browser-based voice recognition
Python – backend logic and session storage
Pandas – table/data formatting

Run Locally
Clone this repo
git clone https://github.com/yourusername/conci-voice-concierge.git
cd conci-voice-concierge

Install dependencies
pip install numpy==1.23.5 bokeh==2.4.3 streamlit==1.30 streamlit-bokeh-events

Run the app
streamlit run app.py

Notes:
Speech recognition works only on Google Chrome due to Web Speech API support.
All state is stored in st.session_state – this is a single-user MVP.



👤 Author
[Dhiya C Jayakumar] – AI Enthusiast | Open Source Builder
www.linkedin.com/in/dhiya-cjayakumar • dhiya.cjayakumar@gmail.com

