# only real time

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib.pyplot as plt
import time

# Load Firebase credentials
cred = credentials.Certificate("/Users/shlokbam/Documents/Code/EDI/firebase_credentials.json")

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://tkph-ace70-default-rtdb.firebaseio.com"
    })

# Function to fetch data from Firebase
def fetch_data():
    ref = db.reference("trucks/truck1/readings")
    data = ref.get()

    if data:
        if isinstance(data, list):
            data = {str(i): entry for i, entry in enumerate(data) if entry}

        df = pd.DataFrame.from_dict(data, orient="index")

        required_columns = {"entry_no", "speed", "payload", "tkph"}
        missing_columns = required_columns - set(df.columns)
        for col in missing_columns:
            df[col] = 0  

        df["payload"] *= 1000  
        df = df.sort_values(by="entry_no", ascending=False)

        return df[["entry_no", "speed", "payload", "tkph"]]
    
    return pd.DataFrame(columns=["entry_no", "speed", "payload", "tkph"])

# Function to plot the graph smoothly
def plot_graph(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["entry_no"], df["speed"], label="Speed (km/h)", marker="o", linestyle="-")
    ax.plot(df["entry_no"], df["payload"], label="Payload (kg)", marker="s", linestyle="--")
    ax.plot(df["entry_no"], df["tkph"], label="TKPH", marker="d", linestyle=":")

    ax.set_xlabel("Entry Number")
    ax.set_ylabel("Values")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.7)
    
    st.pyplot(fig)  # Smoothly update chart

# Streamlit UI
st.title("🚛 Real-time Truck Monitoring Dashboard")
st.subheader("📊 Latest Truck Data")

data_placeholder = st.empty()
chart_placeholder = st.empty()

while True:
    df = fetch_data()

    if not df.empty:
        data_placeholder.dataframe(df)
        with chart_placeholder:
            plot_graph(df)  # Smooth graph update
    else:
        data_placeholder.warning("No data available!")

    time.sleep(3)  # Smooth updates without flickering