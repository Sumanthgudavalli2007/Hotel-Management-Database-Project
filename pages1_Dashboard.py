import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

st.title("📊 Business Dashboard")

try:
    conn = get_connection()

    st.subheader("Room Occupancy Overview")

    df = pd.read_sql(
        "SELECT Status, COUNT(*) as Total FROM Rooms GROUP BY Status",
        conn
    )

    if df.empty:
        st.warning("No data available ⚠️")
    else:
        # 🎨 Professional Bar Chart
        fig = px.bar(
            df,
            x="Status",
            y="Total",
            text="Total",
            color="Status",
            color_discrete_map={
                "Available": "#28B463",     # green
                "Occupied": "#E74C3C",      # red
                "Maintenance": "#F39C12"    # orange
            }
        )

        # ✨ Styling
        fig.update_layout(
            title="Room Status Overview",
            title_x=0.5,
            xaxis_title="Room Status",
            yaxis_title="Number of Rooms",
            template="plotly_white",
            height=450
        )

        fig.update_traces(
            textposition='outside'
        )

        st.plotly_chart(fig, use_container_width=True)

    conn.close()

except Exception as e:
    st.error(f"Database Error: {e}")