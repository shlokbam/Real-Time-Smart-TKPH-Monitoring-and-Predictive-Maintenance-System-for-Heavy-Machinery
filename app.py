# integrated both   

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib.pyplot as plt
import time
import joblib
import numpy as np
import os

# Load Firebase credentials
cred = credentials.Certificate("/Users/shlokbam/Documents/Code/EDI/firebase_credentials.json")

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://tkph-ace70-default-rtdb.firebaseio.com"
    })

# Load trained models
reg_model = joblib.load("Models/regression_model.pkl")
class_model = joblib.load("Models/classification_model.pkl")

# CSV file path
csv_file = "tkph_predictions.csv"

# Streamlit UI
st.set_page_config(page_title="TKPH & Truck Monitoring", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio("📌 Select a Page:", ["Real-time Truck Monitoring", "TKPH-Based Tire Analysis"])

if menu == "Real-time Truck Monitoring":
    st.title("🚛 Real-time Truck Monitoring Dashboard")
    st.subheader("📊 Latest Truck Data")

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

    # Function to plot the graph
    def plot_graph(df):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df["entry_no"], df["speed"], label="Speed (km/h)", marker="o", linestyle="-")
        ax.plot(df["entry_no"], df["payload"], label="Payload (kg)", marker="s", linestyle="--")
        ax.plot(df["entry_no"], df["tkph"], label="TKPH", marker="d", linestyle=":")

        ax.set_xlabel("Entry Number")
        ax.set_ylabel("Values")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.7)
        
        st.pyplot(fig)

    data_placeholder = st.empty()
    chart_placeholder = st.empty()

    while True:
        df = fetch_data()
        if not df.empty:
            data_placeholder.dataframe(df)
            with chart_placeholder:
                plot_graph(df)
        else:
            data_placeholder.warning("No data available!")
        time.sleep(3)
    
    st.markdown("---")
    st.markdown("🔹 **Developed for Predictive Tire Analysis and Truck Monitoring using Machine Learning** 🚀")

elif menu == "TKPH-Based Tire Analysis":
    st.title("🚜 TKPH-Based Tire Analysis System")
    st.write("🔍 Enter the **Vehicle Number** and **TKPH Value** to analyze **Tire Performance, Failure Risk, and Maintenance Needs**.")

    if "tkph_history" not in st.session_state:
        st.session_state.tkph_history = []

    # Sidebar input
    vehicle_no = st.text_input("🚗 Enter Vehicle Number")
    tkph_value = st.number_input("📊 Enter TKPH Value", min_value=0, step=1)
    predict_button = st.button("🔮 Predict")

    if predict_button:
        if not vehicle_no:
            st.error("🚨 Please enter a Vehicle Number!")
        else:
            input_data = np.array([[tkph_value]])
            reg_prediction = reg_model.predict(input_data)
            tire_wear, remaining_life, fuel_consumption = reg_prediction[0]
            class_prediction = class_model.predict(input_data)
            failure_risk, maintenance_alert = class_prediction[0]

            st.session_state.tkph_history.append(tkph_value)
            
            # Display results
            st.subheader("📌 **Predictions:**")
            st.markdown(f"**🛞 Tire Wear:** `{tire_wear:.2f}%`")
            st.progress(int(tire_wear))
            st.markdown(f"**⏳ Remaining Tire Life:** `{remaining_life:.2f} Hours`")
            st.markdown(f"**⛽ Fuel Consumption:** `{fuel_consumption:.2f} L/h`")

            if failure_risk == "High Heat Failure Risk":
                st.error("🚨 **Tire Failure Risk: High Heat Failure Risk!** Reduce load or speed immediately.")
            elif failure_risk == "High Cut Failure Risk":
                st.warning("⚠️ **Tire Failure Risk: High Cut Failure Risk!** Be cautious on rough terrain.")
            else:
                st.success("✅ **Tire Failure Risk: Safe Operating Range**")

            if maintenance_alert:
                st.error("🔧 **Maintenance Alert: Immediate Maintenance Required!**")
            else:
                st.success("⏳ **No Immediate Maintenance Required**")

            new_entry = pd.DataFrame([[vehicle_no, tkph_value, tire_wear, remaining_life, fuel_consumption, failure_risk, maintenance_alert]],
                                     columns=["Vehicle Number", "TKPH Value", "Tire Wear (%)", "Remaining Life (Hours)", "Fuel Consumption (L/h)", "Failure Risk", "Maintenance Alert"])

            if os.path.exists(csv_file):
                new_entry.to_csv(csv_file, mode='a', header=False, index=False)
            else:
                new_entry.to_csv(csv_file, mode='w', header=True, index=False)

            st.success("✅ Entry saved to CSV!")

    st.markdown("---")
    st.markdown("🔹 **Developed for Predictive Tire Analysis and Truck Monitoring using Machine Learning** 🚀")