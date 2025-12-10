# 🐟 Sustainable Fish Aquaculture Monitoring System (IoT + ML)

This project helps fish farmers keep their ponds healthy using:

- **IoT** (ESP32 + sensors) to read water quality  
- **Machine Learning (ML)** to predict if the pond is **Optimal** or **Non-Optimal**  
- **Web Dashboard (Flask + HTML)** to see values and prediction in real time  

The system measures:

- pH  
- Turbidity  
- TDS (Total Dissolved Salts)  
- Air Quality (MQ-135)  
- Temperature  
- Ammonia
- Dissolved Oxygen  

If values go out of safe range, the system shows **Non-Optimal** so that farmers can take action. :contentReference[oaicite:1]{index=1}  

---

## 🔧 Project Parts

1. `esp32/pond_node.ino`  
   - Runs on ESP32  
   - Reads all sensors  
   - Sends data to the web server (Flask app)

2. `ml/train_model.py`  
   - Trains a simple Logistic Regression ML model  
   - Saves `random_forest_model.joblib`

3. `ml/predict.py`  
   - Loads the model  
   - Predicts if the pond is **Optimal** or **Non-Optimal**

4. `web/app.py`  
   - Flask web server  
   - Receives data from ESP32  
   - Uses ML model to predict  
   - Shows a web page with live data

5. `web/templates/index.html`  
   - Simple dashboard page to display values and prediction

---
