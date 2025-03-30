# only model

import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load trained models
reg_model = joblib.load("Models/regression_model.pkl")
class_model = joblib.load("Models/classification_model.pkl")

# CSV file path
csv_file = "tkph_predictions.csv"

# Streamlit UI
st.set_page_config(page_title="TKPH-Based Tire Analysis", layout="wide")
st.title("🚜 TKPH-Based Tire Analysis System")
st.write("🔍 Enter the **Vehicle Number** and **TKPH Value** to analyze **Tire Performance, Failure Risk, and Maintenance Needs**.")

# Initialize session state for trend tracking
if "tkph_history" not in st.session_state:
    st.session_state.tkph_history = []

# Sidebar for input
with st.sidebar:
    vehicle_no = st.text_input("🚗 Enter Vehicle Number")
    tkph_value = st.number_input("📊 Enter TKPH Value", min_value=0, step=1)
    predict_button = st.button("🔮 Predict")

if predict_button:
    if not vehicle_no:
        st.error("🚨 Please enter a Vehicle Number!")
    else:
        input_data = np.array([[tkph_value]])

        # Regression Predictions
        reg_prediction = reg_model.predict(input_data)
        tire_wear, remaining_life, fuel_consumption = reg_prediction[0]

        # Classification Predictions
        class_prediction = class_model.predict(input_data)
        failure_risk, maintenance_alert = class_prediction[0]

        # Store TKPH values for trend tracking
        st.session_state.tkph_history.append(tkph_value)

        # Display results
        st.subheader("📌 **Predictions:**")
        st.markdown(f"**🛞 Tire Wear:** `{tire_wear:.2f}%`")
        st.progress(int(tire_wear))  # Progress bar for tire wear
        st.markdown(f"**⏳ Remaining Tire Life:** `{remaining_life:.2f} Hours`")
        st.markdown(f"**⛽ Fuel Consumption:** `{fuel_consumption:.2f} L/h`")

        # Tire Failure Risk
        if failure_risk == "High Heat Failure Risk":
            st.error("🚨 **Tire Failure Risk: High Heat Failure Risk!** Reduce load or speed immediately.")
        elif failure_risk == "High Cut Failure Risk":
            st.warning("⚠️ **Tire Failure Risk: High Cut Failure Risk!** Be cautious on rough terrain.")
        else:
            st.success("✅ **Tire Failure Risk: Safe Operating Range**")

        # Maintenance Alert
        if maintenance_alert:
            st.error("🔧 **Maintenance Alert: Immediate Maintenance Required!**")
        else:
            st.success("⏳ **No Immediate Maintenance Required**")

         # Rule-based insights
        st.subheader("📊 **Rule-Based Insights:**")
        
        if tkph_value > 170:
            st.warning("⚠️ **Recommendation:** Reduce speed or load.")
        elif 120 <= tkph_value <= 140:
            st.success("✅ **Optimal TKPH Range:** Operating at ideal load.")
        elif 100 <= tkph_value < 120:
            st.info("🔹 **Operating Condition:** Optimize tire selection.")
        
        if tkph_value > 150:
            st.error("🔥 **High Heat Failure Risk!** Consider load adjustment.")
        elif tkph_value < 100:
            st.warning("⚡ **High Cut Failure Risk!** Avoid rough surfaces.")

        # Maintenance Trends
        st.subheader("🛠 **Next Maintenance Prediction:**")
        if tkph_value > 150:
            st.warning("🔧 **High TKPH for 3+ Days → Schedule Maintenance Soon!**")
        elif tkph_value < 120:
            st.success("✅ **Stable TKPH → Extend Next Check by 10 Hours**")

        # Save to CSV
        new_entry = pd.DataFrame([[vehicle_no, tkph_value, tire_wear, remaining_life, fuel_consumption, failure_risk, maintenance_alert]],
                                 columns=["Vehicle Number", "TKPH Value", "Tire Wear (%)", "Remaining Life (Hours)", "Fuel Consumption (L/h)", "Failure Risk", "Maintenance Alert"])
        
        if os.path.exists(csv_file):
            new_entry.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            new_entry.to_csv(csv_file, mode='w', header=True, index=False)

        st.success("✅ Entry saved to CSV!")

# Footer
st.markdown("---")
st.markdown("🔹 **Developed for Predictive Tire Analysis using Machine Learning** 🚀")