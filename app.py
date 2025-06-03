from flask import Flask, render_template, jsonify, request
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import joblib
import numpy as np
import os
import json
from datetime import datetime

app = Flask(__name__)

# Initialize Firebase if not already initialized
try:
    cred = credentials.Certificate("firebase_credentials.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://tkph-ace70-default-rtdb.firebaseio.com"
        })
except Exception as e:
    print(f"Firebase initialization failed: {e}")

# Load trained models
try:
    reg_model = joblib.load("models/regression_model.pkl")
    class_model = joblib.load("models/classification_model.pkl")
except Exception as e:
    print(f"Model loading failed: {e}")
    reg_model = None
    class_model = None

# CSV file path
csv_file = "tkph_predictions.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitoring')
def monitoring():
    return render_template('monitoring.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/api/truck-data')
def get_truck_data():
    try:
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

            return jsonify({
                "status": "success",
                "data": df[["entry_no", "speed", "payload", "tkph"]].to_dict(orient="records")
            })
        else:
            return jsonify({
                "status": "empty",
                "message": "No data available"
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        vehicle_no = data.get('vehicleNumber')
        tkph_value = float(data.get('tkphValue'))
        
        if not vehicle_no:
            return jsonify({"status": "error", "message": "Vehicle number required"})
            
        input_data = np.array([[tkph_value]])
        
        # Regression Predictions
        reg_prediction = reg_model.predict(input_data)
        tire_wear, remaining_life, fuel_consumption = reg_prediction[0]
        
        # Classification Predictions
        class_prediction = class_model.predict(input_data)
        failure_risk_code, maintenance_alert = class_prediction[0]
        
        # Convert failure risk code to text
        risk_map = {
            0: "Safe Operating Range",
            1: "Normal Risk",
            2: "High Cut Failure Risk",
            3: "High Heat Failure Risk"
        }
        failure_risk = risk_map.get(failure_risk_code, "Unknown Risk")
        
        # Rule-based insights
        insights = []
        if tkph_value > 170:
            insights.append({"type": "warning", "message": "Reduce speed or load."})
        elif 120 <= tkph_value <= 140:
            insights.append({"type": "success", "message": "Operating at ideal load."})
        elif 100 <= tkph_value < 120:
            insights.append({"type": "info", "message": "Optimize tire selection."})
        
        if tkph_value > 150:
            insights.append({"type": "danger", "message": "High Heat Failure Risk! Consider load adjustment."})
        elif tkph_value < 100:
            insights.append({"type": "warning", "message": "High Cut Failure Risk! Avoid rough surfaces."})
            
        # Save to CSV
        new_entry = pd.DataFrame([[vehicle_no, tkph_value, tire_wear, remaining_life, fuel_consumption, failure_risk, maintenance_alert]],
                                columns=["Vehicle Number", "TKPH Value", "Tire Wear (%)", "Remaining Life (Hours)", 
                                         "Fuel Consumption (L/h)", "Failure Risk", "Maintenance Alert"])
        
        if os.path.exists(csv_file):
            new_entry.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            new_entry.to_csv(csv_file, mode='w', header=True, index=False)
            
        return jsonify({
            "status": "success",
            "data": {
                "tire_wear": round(tire_wear, 2),
                "remaining_life": round(remaining_life, 2),
                "fuel_consumption": round(fuel_consumption, 2),
                "failure_risk": failure_risk,
                "maintenance_alert": bool(maintenance_alert),
                "insights": insights
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

# History endpoint for tracking past predictions
@app.route('/api/history')
def history():
    try:
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            return jsonify({
                "status": "success",
                "data": df.to_dict(orient="records")
            })
        else:
            return jsonify({
                "status": "empty",
                "message": "No history available"
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)