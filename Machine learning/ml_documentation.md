# Machine Learning Module – Smart Fish Aquaculture System

The **Machine Learning (ML)** module is responsible for analysing sensor data
from the fish pond and predicting whether the aquaculture environment is
**Optimal** or **Non-Optimal**.

This module works together with:
- The **hardware** (ESP32 + sensors)
- The **web application** (Flask dashboard)
- Optionally, the **IoT dashboard** (Node-RED + MQTT)

---

## 📁 1. Folder Structure

```text
machine_learning/
│
├── dataset/
│   └── aquaculture_dataset_rf_only.csv
│
├── models/
│   └── random_forest_model.joblib
│
├── scripts/
│   ├── train_model_realdata.py
│   └── predict_rf.py
│
├── notebooks/
│   └── model_development.ipynb      (optional)
│
├── ml_results/
│   ├── confusion_matrix.png         (optional)
│   └── accuracy_plot.png            (optional)
│
└── ml_documentation.md              ← (this file)
```

---

## 📊 2. Dataset Description

The main dataset used for training is:

- **File:** `aquaculture_dataset_rf_only.csv`
- **Location:** `machine_learning/dataset/`

Typical columns include:

- `Air Quality (ppm)` – MQ135 gas sensor
- `Temp (°C)` – water temperature
- `Turbidity` – water clarity (NTU)
- `TDS (ppm)` – Total Dissolved Solids
- `pH` – acidity / alkalinity
- `NH3 (mg/L)` – ammonia concentration
- `DO (mg/L)` – dissolved oxygen
- `Aquaculture Environment Status` – label (Optimal / Non-Optimal)

During preprocessing (inside the training script):

- Columns are renamed to a Python-friendly format:
  - `air_quality`, `temperature`, `turbidity`, `tds`, `ph`, `nh3`, `do`, `status`
- The `status` column is encoded as:
  - `1` → **Optimal**
  - `0` → **Non-Optimal**

---

## 🤖 3. Model Used – Random Forest Classifier

The current ML model is a **Random Forest Classifier**:

- Handles non-linear decision boundaries
- Robust to noise in sensor measurements
- Works well with a mix of different scale features
- Suitable for small to medium-sized datasets

The trained model is stored as:

- **File:** `random_forest_model.joblib`
- **Location:** `machine_learning/models/`

This file is loaded in:
- `machine_learning/scripts/predict_rf.py`
- The Flask web app (`web_app/app.py`) for live predictions

---

## 🧪 4. Training Script – `train_model_realdata.py`

This script:

1. Loads `aquaculture_dataset_rf_only.csv`
2. Renames columns to clean Python names
3. Encodes the target labels (Optimal / Non-Optimal)
4. Splits the data into training and testing sets
5. Trains a Random Forest Classifier
6. Evaluates the model (accuracy, confusion matrix, classification report)
7. Saves the trained model as `random_forest_model.joblib`

Typical usage from the terminal:

```bash
cd machine_learning/scripts
python train_model_realdata.py
```

After running, you should see:

- Printed accuracy and metrics
- Updated `random_forest_model.joblib` in `../models/`

---

## 📤 5. Prediction Script – `predict_rf.py`

This script loads the trained Random Forest model and exposes a helper function:

```python
predict_status_rf(air_quality, temperature, turbidity, tds, ph, nh3, do)
```

It returns:

- `"Optimal"` or `"Non-Optimal"`

This same function can be imported and used inside the **Flask app**:

```python
from machine_learning.scripts.predict_rf import predict_status_rf
```

or by adjusting the import path based on your project layout.

---

## 🌐 6. Integration with Web Application

In the Flask backend (`web_app/app.py`):

1. Sensor data is received from ESP32 or another source
2. Values are arranged in the correct feature order:
   ```python
   [air_quality, temperature, turbidity, tds, ph, nh3, do]
   ```
3. The model is loaded from:
   ```python
   ../machine_learning/models/random_forest_model.joblib
   ```
4. The prediction result is added to a `latest_data` dictionary
5. The dashboard displays:
   - Live sensor values
   - Predicted pond status (Optimal / Non-Optimal)

---

## 🔄 7. How to Retrain with a New Dataset

If you collect new or larger datasets:

1. Replace or add your new CSV file in:
   ```text
   machine_learning/dataset/
   ```
2. Update `train_model_realdata.py` to point to your new file name.
3. Run:
   ```bash
   cd machine_learning/scripts
   python train_model_realdata.py
   ```
4. A new `random_forest_model.joblib` will be created.
5. Restart the Flask app so it uses the updated model.

---

## ✅ 8. Summary

- The **ML module** transforms raw sensor readings into a clear decision:
  - **Optimal vs Non-Optimal aquaculture environment**
- The key assets are:
  - `aquaculture_dataset_rf_only.csv` → Real dataset
  - `random_forest_model.joblib` → Trained Random Forest model
  - `train_model_realdata.py` → Training logic
  - `predict_rf.py` → Inference (prediction) logic
- This module integrates seamlessly with both:
  - The **hardware layer** (ESP32 + sensors)
  - The **web layer** (Flask dashboard + APIs)

Together, they form a complete **IoT + ML–based smart fish aquaculture monitoring system**.
