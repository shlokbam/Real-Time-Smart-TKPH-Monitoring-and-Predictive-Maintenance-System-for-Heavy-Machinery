# Real-Time Smart TKPH Monitoring and Predictive Maintenance System for Heavy Machinery

A comprehensive solution for monitoring Ton-Kilometers Per Hour (TKPH) values and predicting maintenance needs for heavy machinery tires.

## 📋 Overview

This system integrates real-time monitoring with predictive analytics to help mining and construction companies optimize tire performance, reduce maintenance costs, and prevent unexpected failures. The application tracks key metrics like speed, payload, and TKPH values, then uses machine learning to predict tire wear, remaining life, failure risks, and maintenance needs.

## 🚀 Features

- **Real-time Truck Monitoring Dashboard**
  - Live tracking of speed, payload, and TKPH values
  - Visual representation through dynamic graphs
  - Automatic data refresh every 3 seconds

- **TKPH-Based Tire Analysis System**
  - Predictive analysis of tire wear percentage
  - Estimation of remaining tire life in hours
  - Fuel consumption prediction
  - Tire failure risk classification
  - Maintenance alerts based on current conditions
  - Historical data storage in CSV format

## 🔧 Technology Stack

- **Frontend**: HTML, CSS and JS
- **Backend**: Python (Flask)
- **Database**: Firebase Realtime Database
- **Machine Learning**: scikit-learn (Random Forest models)
- **Data Visualization**: Matplotlib
- **Data Processing**: Pandas, NumPy

## 📊 Machine Learning Models

The system uses two trained models:
1. **Regression Model**: Predicts continuous values (tire wear, remaining life, fuel consumption)
2. **Classification Model**: Predicts categorical outcomes (failure risk, maintenance needs)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Real-Time-Smart-TKPH-Monitoring.git
cd Real-Time-Smart-TKPH-Monitoring
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Firebase:
   - Create a Firebase project
   - Generate a private key JSON file
   - Update the path in the code to your Firebase credentials file

4. Run the application:
```bash
streamlit run app.py
```

## 📂 File Structure

- `app.py`: Main application integrating both monitoring and analysis features
- `real_time_data.py`: Standalone real-time monitoring module
- `model_predictions.py`: Standalone TKPH analysis module
- `data.py`: Script for generating synthetic training data
- `processing.py`: Script for training and saving machine learning models
- `Models/`: Directory containing trained ML models
  - `regression_model.pkl`: For predicting continuous values
  - `classification_model.pkl`: For predicting categorical outcomes
- `tkph_predictions.csv`: Storage for historical predictions

## 🔄 Workflows

### Real-time Monitoring
1. Data is continuously fetched from Firebase
2. Dashboard updates with latest values every 3 seconds
3. Dynamic visualization shows trends in speed, payload, and TKPH

### Predictive Analysis
1. User inputs vehicle number and TKPH value
2. System predicts tire wear, remaining life, and fuel consumption
3. System classifies failure risk and maintenance needs
4. Results are saved to CSV for historical tracking

## 🔍 TKPH Explained

TKPH (Ton-Kilometers Per Hour) is a critical metric for tire performance in heavy machinery:
- Calculated as: TKPH = Average Speed × Average Load
- Higher TKPH values indicate increased heat generation in tires
- Exceeding a tire's TKPH rating leads to accelerated wear and potential failure

## 🚨 Safety Guidelines

- Keep TKPH values within the manufacturer's recommended range
- Immediate action is required when "High Heat Failure Risk" is detected
- Regular maintenance should be scheduled based on system alerts

## 🔮 Future Enhancements

- Multi-vehicle tracking and comparison
- Mobile application for on-the-go monitoring
- Integration with tire manufacturer databases for model-specific recommendations
- Advanced anomaly detection for early warning signs

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Contributors

- Your Name - Initial work

## 📧 Contact

For questions or support, please contact: shlokbam19103@gmail.com
