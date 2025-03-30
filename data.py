import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic TKPH values (between 50 and 600)
tkph_values = np.random.randint(50, 601, 1000)  # 1000 samples

# Apply formulas
tire_wear = 100 * (1 - np.exp(-0.001 * tkph_values))  # Exponential wear model
remaining_life = 1200 / (1 + 0.002 * tkph_values)  # Inverse relation
fuel_consumption = 2.5 + 0.015 * tkph_values + np.sin(tkph_values / 50)  # Linear + oscillations

# Categorizing Tire Failure Risk
failure_risk = np.digitize(tkph_values, bins=[150, 300, 450, 600])  # 0=Low, 1=Medium, 2=High, 3=Critical

# Maintenance Alert (1 if risk is High or Critical, else 0)
maintenance_alert = np.where(failure_risk >= 2, 1, 0)

# Create DataFrame
df = pd.DataFrame({
    "TKPH": tkph_values,
    "Tire Wear (%)": tire_wear,
    "Remaining Tire Life (Hours)": remaining_life,
    "Fuel Consumption (L/h)": fuel_consumption,
    "Tire Failure Risk": failure_risk,
    "Maintenance Alert": maintenance_alert
})

# Save dataset
df.to_csv("synthetic_tkph_data.csv", index=False)

# Display first 5 rows
print(df.head())
