import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import base64

# Import consolidation function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from consolidation_algorithm import consolidate_shipments


# -----------------------------
# Load Video File
# -----------------------------
video_path = os.path.join(os.path.dirname(__file__), "..", "assets", "background.mp4")

with open(video_path, "rb") as f:
    video_bytes = f.read()

video_base64 = base64.b64encode(video_bytes).decode()


# -----------------------------
# Background Video + CSS
# -----------------------------
st.markdown(
    f"""
<style>

/* Fullscreen background video */
#bg-video {{
position: fixed;
top: 0;
left: 0;
width: 100vw;
height: 100vh;
object-fit: cover;
z-index: -2;
}}

/* Dark overlay */
.video-overlay {{
position: fixed;
top: 0;
left: 0;
width: 100vw;
height: 100vh;
background: rgba(0,0,0,0.55);
z-index: -1;
}}

/* Remove Streamlit background */
.stApp {{
background: transparent;
}}

[data-testid="stHeader"] {{
background: transparent;
}}

/* Dashboard panel */
.block-container {{
background: rgba(255,255,255,0.92);
padding: 30px;
border-radius: 15px;
}}

</style>

<video autoplay muted loop id="bg-video">
<source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
</video>

<div class="video-overlay"></div>
""",
    unsafe_allow_html=True
)


# -----------------------------
# Title
# -----------------------------
st.title("🚚 AI Load Consolidation Optimization Engine")
st.write("Upload shipment dataset to optimize truck loads.")


# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


if uploaded_file is not None:

    # Create dataframe
    df = pd.read_csv(uploaded_file)

    # Show only first 10 rows for demo
    st.subheader("Sample of Uploaded Dataset")
    st.dataframe(df.head(10))

    # Convert delivery date
    df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"])

    # Group shipments by date
    grouped = df.groupby("Delivery_Date")

    trip_chart_data = []
    util_chart_data = []

    truck_capacity = 1000

    for date, group in grouped:

        trucks, weights = consolidate_shipments(group)

        # Trips comparison
        trip_chart_data.append({
            "Date": date.date(),
            "Scenario": "Before Optimization",
            "Trips": len(group)
        })

        trip_chart_data.append({
            "Date": date.date(),
            "Scenario": "After Optimization",
            "Trips": len(trucks)
        })

        # Utilization
        for i, w in enumerate(weights):

            util_chart_data.append({
                "Date": date.date(),
                "Truck": f"Truck {i+1}",
                "Utilization %": (w / truck_capacity) * 100
            })


    trip_df = pd.DataFrame(trip_chart_data)
    util_df = pd.DataFrame(util_chart_data)


    # -----------------------------
    # Select Date
    # -----------------------------
    available_dates = trip_df["Date"].unique()

    selected_date = st.selectbox(
        "Select Delivery Date for Analysis",
        available_dates
    )


    # -----------------------------
    # Trips Chart
    # -----------------------------
    st.subheader(f"🚚 Trips Comparison for {selected_date}")

    trip_filtered = trip_df[trip_df["Date"] == selected_date]

    fig1 = px.bar(
        trip_filtered,
        x="Scenario",
        y="Trips",
        color="Scenario",
        barmode="group",
        title="Trips Before vs After Optimization"
    )

    st.plotly_chart(fig1, use_container_width=True)


    # -----------------------------
    # Utilization Chart
    # -----------------------------
    st.subheader(f"📊 Truck Utilization on {selected_date}")

    util_filtered = util_df[util_df["Date"] == selected_date]

    fig2 = px.bar(
        util_filtered,
        x="Truck",
        y="Utilization %",
        color="Utilization %",
        title="Truck Utilization"
    )

    st.plotly_chart(fig2, use_container_width=True)