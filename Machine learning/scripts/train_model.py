import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import joblib
import warnings
warnings.filterwarnings('ignore')

# Reproducibility
np.random.seed(42)

# Generate synthetic dataset
n_samples = 25000
data = {
    'Air Quality (ppm)': np.random.uniform(90, 150, n_samples),
    'Temp (°C)': np.random.uniform(26, 34, n_samples),
    'Humidity (%)': np.random.uniform(70, 90, n_samples),
    'Turbidity': np.random.uniform(35, 60, n_samples),
    'TDS (ppm)': np.random.uniform(90, 400, n_samples),
    'pH': np.random.uniform(6.9, 8.6, n_samples),
    'NH3 (mg/L)': np.random.uniform(0, 3, n_samples),
    'DO (mg/L)': np.random.uniform(5, 8, n_samples)
}
df = pd.DataFrame(data)

# Status assignment
def assign_status(row):
    if (7.1 <= row['pH'] <= 8.3 and 
        row['NH3 (mg/L)'] <= 1.8 and 
        26.5 <= row['Temp (°C)'] <= 33 and 
        row['DO (mg/L)'] >= 5.8 and 
        110 <= row['TDS (ppm)'] <= 350):
        return 'Optimal'
    elif (row['pH'] < 6.92 or row['pH'] > 8.45 or 
          row['NH3 (mg/L)'] > 2.2 or 
          row['Temp (°C)'] < 26.1 or row['Temp (°C)'] > 33.8 or 
          row['DO (mg/L)'] < 5.1 or 
          row['TDS (ppm)'] < 92 or row['TDS (ppm)'] > 390):
        return 'Non-Optimal'
    else:
        return np.random.choice(['Optimal', 'Non-Optimal'], p=[0.95, 0.05])

df['Aquaculture Environment Status'] = df.apply(assign_status, axis=1)

# Timestamp generation
start_time = datetime(2025, 3, 1, 0, 0, 0)
df['Timestamp'] = [start_time + timedelta(seconds=5*i) for i in range(n_samples)]

# Column arrangement
df = df[['Timestamp', 'Air Quality (ppm)', 'Temp (°C)', 'Humidity (%)', 'Turbidity', 
         'TDS (ppm)', 'pH', 'NH3 (mg/L)', 'DO (mg/L)', 'Aquaculture Environment Status']]

# Print class balance
print("Class Distribution:")
print(df['Aquaculture Environment Status'].value_counts(normalize=True))

# ML prep
X = df.drop(columns=['Timestamp', 'Aquaculture Environment Status'])
y = df['Aquaculture Environment Status'].map({'Optimal': 1, 'Non-Optimal': 0})
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nRandom Forest Accuracy: {accuracy:.4f}")

# Save dataset
df.to_csv("aquaculture_dataset_rf_only.csv", index=False)
print("Dataset saved as 'aquaculture_dataset_rf_only.csv'")

# Preview
print("\nSample data:")
print(df.head())

# save model
res = joblib.dump(rf_model, 'random_forest_model.joblib')
print("model saved", res)