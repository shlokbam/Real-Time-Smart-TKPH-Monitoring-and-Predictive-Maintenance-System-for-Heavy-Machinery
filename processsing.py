import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("synthetic_tkph_data.csv")

# Define features and targets
X = df[['TKPH']]

y_reg = df[['Tire Wear (%)', 'Remaining Tire Life (Hours)', 'Fuel Consumption (L/h)']]
y_class = df[['Tire Failure Risk', 'Maintenance Alert']]

# Split the dataset
X_train, X_test, y_train_reg, y_test_reg, y_train_class, y_test_class = train_test_split(
    X, y_reg, y_class, test_size=0.2, random_state=42
)

# Train regression model
reg_model = RandomForestRegressor(n_estimators=100, random_state=42)
reg_model.fit(X_train, y_train_reg)

# Train classification model
class_model = RandomForestClassifier(n_estimators=100, random_state=42)
class_model.fit(X_train, y_train_class)

# Save models
joblib.dump(reg_model, "regression_model.pkl", protocol=2)
joblib.dump(class_model, "classification_model.pkl", protocol=2)



print("Models trained and saved successfully!")
