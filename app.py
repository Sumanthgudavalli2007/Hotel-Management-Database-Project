import streamlit as st
from database import get_connection

st.set_page_config(page_title="Hotel Management System", layout="wide")

# 🎨 Custom Style
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #2E86C1;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F4F6F7;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-title">🏨 Grand Vista Hotel Management System</p>', unsafe_allow_html=True)
st.markdown("---")

st.write("### Welcome, Admin 👋")
st.info("Manage rooms, bookings, and hotel operations efficiently.")

# 🔹 Columns
col1, col2, col3 = st.columns(3)

# System Status
with col1:
    st.markdown('<div class="card">🟢<br><b>System Status</b><br>Online</div>', unsafe_allow_html=True)

# DB Status
with col2:
    try:
        conn = get_connection()
        status = "🟢 Connected"
        conn.close()
    except:
        status = "🔴 Not Connected"

    st.markdown(f'<div class="card">💾<br><b>Database</b><br>{status}</div>', unsafe_allow_html=True)

# Team
with col3:
    st.markdown('<div class="card">👨‍💻<br><b>Team</b><br>4 Members</div>', unsafe_allow_html=True)

st.markdown("---")

# Extra Section
st.subheader("📌 Features")
st.write("""
✔ Room Management  
✔ Booking System  
✔ Guest Tracking  
✔ Real-time Dashboard  
""")