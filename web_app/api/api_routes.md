# API Routes Documentation – Smart Fish Aquaculture System

This document explains all API endpoints provided by the Flask backend of the  
**Smart Fish Aquaculture Monitoring & Prediction System**.

These APIs are used by:
- ESP32 microcontroller (sending sensor data)
- Web dashboard (fetching latest data)
- Node-RED (optional integration)
- Postman / Testing tools

---

# 📘 API Overview

| Route           | Method | Purpose |
|----------------|--------|---------|
| `/`            | GET    | Loads the dashboard webpage |
| `/data`        | POST   | Receives sensor data from ESP32 |
| `/latest_data` | GET    | Returns latest sensor values + ML prediction |

---

# 🟦 **1. GET /**  
### **Purpose:**  
Loads the **web dashboard** (`templates/index.html`), which displays:

- Latest sensor readings  
- ML-predicted pond status  
- Auto-refreshing UI (optional)

### **Response:**  
HTML webpage.

---

# 🟩 **2. POST /data**  
### **Purpose:**  
Receives real-time sensor readings from ESP32 or Postman.

### 📥 **Required form-data fields:**

| Field        | Type  | Example | Description |
|-------------|--------|---------|-------------|
| `air_quality` | float | 120.5 | Air quality (ppm) – MQ135 |
| `temperature` | float | 28.4 | Water temperature (°C) |
| `turbidity`  | float | 40 | Water turbidity (NTU) |
| `tds`        | float | 250 | Total dissolved solids |
| `ph`         | float | 7.2 | Acidity (0–14) |
| `nh3`        | float | 0.5 | Ammonia level (mg/L) |
| `do`         | float | 6.4 | Dissolved oxygen (mg/L) |

### 📤 **Response JSON (Success):**

```json
{
  "status": "ok",
  "prediction": "Optimal"
}
```

### 📤 **Response JSON (Error):**

```json
{
  "status": "error",
  "message": "Error details here"
}
```

---

# 🟧 Example POST Request (Postman)

Method: **POST**  
URL: `http://127.0.0.1:5000/data`  
Body Type: **form-data**

| Key          | Value |
|--------------|--------|
| air_quality  | 120 |
| temperature  | 29 |
| turbidity    | 40 |
| tds          | 250 |
| ph           | 7.1 |
| nh3          | 0.4 |
| do           | 6.0 |

---

# 🟥 Example POST Request (ESP32 Code Snippet)

```cpp
HTTPClient http;
http.begin("http://YOUR_IP:5000/data");
http.addHeader("Content-Type", "application/x-www-form-urlencoded");

String postData =
  "air_quality=" + String(air_quality) +
  "&temperature=" + String(tempC) +
  "&turbidity=" + String(turbidity) +
  "&tds=" + String(tdsValue) +
  "&ph=" + String(pHValue) +
  "&nh3=" + String(nh3Value) +
  "&do=" + String(doValue);

int response = http.POST(postData);
String responseBody = http.getString();
Serial.println(responseBody);

http.end();
```

Replace `YOUR_IP` with the IP of your laptop running Flask.

---

# 🟨 **3. GET /latest_data**  
### **Purpose:**  
Used by dashboard / Node-RED to fetch the latest:

- Sensor readings  
- ML prediction  
- Time-stamped values (optional)

### 📤 **Example JSON Response:**

```json
{
  "air_quality": 120,
  "temperature": 29.1,
  "turbidity": 41,
  "tds": 256,
  "ph": 7.1,
  "nh3": 0.4,
  "do": 6.5,
  "prediction": "Optimal"
}
```

This is refreshed every time `/data` receives new values.

---

# 🔄 Workflow Summary

```
ESP32 → POST /data → Flask → Prediction → Dashboard
Dashboard → GET /latest_data → Live Updates
Node-RED → GET /latest_data → Graphs / Alerts
```

---

# 🏁 Final Notes

- All numerical inputs must be **float values**.  
- pH is automatically clamped between **0 and 14** for safety.  
- The same feature order used in ML training is used in prediction.  
- The API is designed to be simple, fast, and IoT-friendly.

This documentation should be placed in:

```
web_app/api/api_routes.md
```

so future developers, evaluators, and contributors can easily understand how your backend works.

