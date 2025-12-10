# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
import pandas as pd
import requests
import io

# Initialize Flask app and enable CORS
app = Flask(__name__)  # Fixed _name_ to __name__
CORS(app)

# Load the trained model and label encoder
model = joblib.load(r"C:\Users\rraje\OneDrive\Desktop\MINI\aquaculture_model.pkl")
label_encoder = joblib.load(r"C:\Users\rraje\OneDrive\Desktop\MINI\label_encoder.pkl")

# Function to fetch live data from ThingSpeak
def fetch_live_data():
    # Replace with your ThingSpeak channel ID and API key
    url = "https://api.thingspeak.com/channels/2896310/feeds.csv?api_key=4BAGCC8LKY97FYG9&results=1"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch live data from ThingSpeak")
    
    data = pd.read_csv(io.StringIO(response.text))
    data.columns = data.columns.str.strip()
    
    # Map ThingSpeak fields to dataset columns
    relevant_data = data[['field1', 'field2', 'field3', 'field4', 'field5', 'field6']]
    relevant_data.columns = ['Air Quality (MQ-135, ppm)', 'Temp (AHT11, °C)', 'Humidity (AHT11, %)', 
                             'Turbidity', 'TDS', 'pH']
    
    return relevant_data.iloc[0].to_dict(), relevant_data.values[0].reshape(1, -1)

# Prediction logic
def get_prediction():
    raw_data, live_data = fetch_live_data()
    prediction = model.predict(live_data)
    predicted_status = label_encoder.inverse_transform(prediction)[0]
    return raw_data, predicted_status

# Route for live prediction
@app.route('/aquaculture-live-data', methods=['GET'])
def aquaculture_live_data():
    try:
        raw_data, predicted_status = get_prediction()
        return jsonify({
            "predicted_status": predicted_status,
            "sensor_data": raw_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':  # Fixed _name_ and _main_ to __name__ and __main__
    app.run(debug=True, host='0.0.0.0', port=5000)