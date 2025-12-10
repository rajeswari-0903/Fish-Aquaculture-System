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
├── api/
│   └── api_routes.md
│
└── dashboard_screenshots/
    └── webpage_preview.png
```

---

## 🌐 2. Main Application File – `app.py`

This is the core Flask backend responsible for:

### ✔ Receiving sensor data  
Endpoint: **POST /data**

The ESP32 (or Postman for testing) sends:

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

- `aquaculture_model.pkl`  
- `label_encoder.pkl`  

from:

```
machine_learning/models/
```

Then calls a helper:

```python
predict_status(...)
```

### ✔ Displaying results on a webpage  
Rendered at route:

```
GET /
```

This loads `templates/index.html` and displays the live data.

---

## 🧪 3. API Endpoints

### 🔹 **POST /data**
Used by ESP32 to send readings.

Example form data:

```
air_quality=120
temperature=29
turbidity=40
tds=250
ph=7.1
nh3=0.5
do=6.0
```

Response JSON:

```json
{
  "status": "ok",
  "prediction": "Optimal"
}
```

### 🔹 **GET /latest_data**
Used by AJAX or Node-RED to fetch the latest sensor values.

Response:

```json
{
  "air_quality": ...,
  "temperature": ...,
  "turbidity": ...,
  "tds": ...,
  "ph": ...,
  "nh3": ...,
  "do": ...,
  "prediction": "Optimal"
}
```

---

## 🖥 4. Frontend Files

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

## 🔧 5. Running the Web App

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

### Step 4 — Test with Postman or ESP32

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
- ML Module (.pkl model + encoder)
- Node-RED Dashboard (optional)

This makes the system ready for **academic submission**, **demonstrations**, and **future expansion**.

