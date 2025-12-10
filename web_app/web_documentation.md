# Web Application Module – Smart Fish Aquaculture System

The **web application** is the user interface of the Smart Fish Aquaculture System.  
It displays real-time sensor data and the machine learning prediction (Optimal / Non-Optimal).  
This module integrates the **ESP32 hardware**, **machine learning model**, and **dashboard UI**.

---

## 📁 1. Folder Structure

```text
web_app/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   └── styles.css
│
└── dashboard_screenshots/
    |── non optimal results.png
    └── optimal results.png
```

---

## 🌐 2. Main Application File – `app.py`

This is the core Flask backend responsible for:

### ✔ Receiving sensor data  

The ESP32 sends:

- air_quality  
- temperature  
- turbidity  
- tds  
- ph  
- nh3  
- do  

Flask extracts these values, validates pH range, and performs ML prediction.

### ✔ Storing latest sensor values  
The app maintains a dictionary:

```python
latest_data = {
    "air_quality": ...,
    "temperature": ...,
    "turbidity": ...,
    "tds": ...,
    "ph": ...,
    "nh3": ...,
    "do": ...,
    "prediction": ...
}
```

### ✔ Updating prediction using the ML model  
`app.py` loads:

- `random_forest_model.joblib`

from:

```
machine_learning/models/
```

Then calls a helper:

```python
predict_status(...)
```


## 🖥 3. Frontend Files

### 📄 `templates/index.html`

Displays:

- Sensor values in a table or cards
- The **pond status**
- Control buttons (optional)
- Auto-refresh via JavaScript (optional)

Supports Bootstrap or custom CSS.

---

### 🎨 `static/styles.css`

Controls page styling:

- Colors
- Layout
- Fonts
- Table and card design

You may customize it to match your theme.

---

## 🔧 4. Running the Web App

### Step 1 — Install requirements

```
pip install -r requirements.txt
```

### Step 2 — Start the server

```
python app.py
```

### Step 3 — Open in browser

```
http://127.0.0.1:5000/
```

or on your Wi-Fi network:

```
http://<your-ip>:5000/
```

### Step 4 — Test with ESP32

Send POST data to:

```
/data
```

---

## 🧩 6. Integration With Machine Learning Module

- `app.py` imports your final model using `joblib.load`
- It uses the same input order as your training set
- The prediction label is added to the dashboard

Working pipeline:

```
ESP32 → Flask → Model Prediction → Web Dashboard / JSON API
```

---

## 📘 7. Advantages of This Web Module

- Lightweight web server  
- Easy to deploy on local machine or Raspberry Pi  
- Real-time dashboard updates  
- Simple API integration  
- Uses your fully trained ML model  

---

## 🏁 8. Summary

The web module completes the project by allowing **real-time monitoring** and **AI-driven decision-making** for fish aquaculture.  
It communicates seamlessly with:

- Hardware (ESP32)
- ML Module (.joblib model + encoder)

This makes the system ready for **academic submission**, **demonstrations**, and **future expansion**.

