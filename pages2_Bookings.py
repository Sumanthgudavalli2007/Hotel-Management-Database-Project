import streamlit as st
import pandas as pd
from database import get_connection, execute_query

st.title("📅 Booking Management")

# Use FORM (fixes button issue)
with st.form("booking_form"):

    st.subheader("New Booking")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    phone = st.text_input("Phone")

    room_id = st.number_input("Room ID", min_value=1)
    check_in = st.date_input("Check-In Date")
    check_out = st.date_input("Check-Out Date")

    submit = st.form_submit_button("Book Room")

    if submit:

        if first_name.strip() == "" or last_name.strip() == "":
            st.warning("Please enter guest details ⚠️")

        elif check_out <= check_in:
            st.error("Check-out must be after check-in ❌")

        else:
            try:
                conn = get_connection()

                # Insert Guest
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Guests (FirstName, LastName, Phone) VALUES (?, ?, ?)",
                    (first_name, last_name, phone)
                )
                conn.commit()

                # Get GuestID
                guest_id = int(pd.read_sql(
                    "SELECT TOP 1 GuestID FROM Guests ORDER BY GuestID DESC",
                    conn
                ).iloc[0][0])

                # Get Room Price
                room_data = pd.read_sql(
                    f"SELECT PricePerNight FROM Rooms WHERE RoomID={int(room_id)}",
                    conn
                )

                if room_data.empty:
                    st.error("Invalid Room ID ❌")

                else:
                    price = float(room_data.iloc[0][0])

                    # Calculate total
                    days = (check_out - check_in).days
                    total_amount = float(days * price)

                    # Insert Booking
                    cursor.execute(
                        """INSERT INTO Bookings 
                        (GuestID, RoomID, CheckInDate, CheckOutDate, TotalAmount)
                        VALUES (?, ?, ?, ?, ?)""",
                        (guest_id, int(room_id), check_in, check_out, total_amount)
                    )

                    # Update Room
                    cursor.execute(
                        "UPDATE Rooms SET Status='Occupied' WHERE RoomID=?",
                        (int(room_id),)
                    )

                    conn.commit()
                    conn.close()

                    st.success("Booking successful! ✅")

                    # 🔥 Refresh page automatically
                    st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# SHOW BOOKINGS
# =========================

st.subheader("All Bookings")

try:
    conn = get_connection()

    df = pd.read_sql("""
        SELECT 
            b.BookingID,
            g.FirstName + ' ' + g.LastName AS GuestName,
            b.RoomID,
            b.CheckInDate,
            b.CheckOutDate,
            b.TotalAmount
        FROM Bookings b
        JOIN Guests g ON b.GuestID = g.GuestID
        ORDER BY b.BookingID DESC
    """, conn)

    st.dataframe(df, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Database Error: {e}")