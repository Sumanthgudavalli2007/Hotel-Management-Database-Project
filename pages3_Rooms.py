import streamlit as st
import pandas as pd
from database import get_connection, execute_query

st.title("🛏️ Room Management")

# =========================
# ADD ROOM
# =========================
with st.form("room_form"):

    st.subheader("Add New Room")

    room_number = st.text_input("Room Number")
    room_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "Deluxe"])
    price = st.number_input("Price Per Night", min_value=500 )

    submit = st.form_submit_button("Add Room")

    if submit:

        if room_number.strip() == "":
            st.warning("Please enter Room Number ⚠️")

        else:
            try:
                query = """
                INSERT INTO Rooms (RoomNumber, RoomType, PricePerNight, Status)
                VALUES (?, ?, ?, ?)
                """

                execute_query(
                    query,
                    (room_number.strip(), room_type, float(price), "Available")
                )

                st.success("Room added successfully! ✅")

                # 🔄 Refresh page
                st.rerun()

            except Exception as e:
                # ✅ Handle duplicate room number
                if "UNIQUE" in str(e) or "duplicate" in str(e).lower():
                    st.error("Room number already exists ❌")
                else:
                    st.error(f"Error: {e}")

# =========================
# VIEW ROOMS
# =========================
st.subheader("All Rooms")

try:
    conn = get_connection()

    df = pd.read_sql("""
        SELECT 
            RoomID,
            RoomNumber,
            RoomType,
            PricePerNight,
            Status
        FROM Rooms
        ORDER BY RoomID DESC
    """, conn)

    st.dataframe(df, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Database Error: {e}")