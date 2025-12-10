# Hardware Documentation – Smart Fish Aquaculture System

This folder contains all hardware-related elements used in the Smart Fish Aquaculture Monitoring System.  
The hardware subsystem is responsible for collecting environmental data from the fish pond using sensors and transmitting it to the server for Machine Learning–based prediction and dashboard display.

---

## 📌 1. Purpose of the Hardware Module

The goal of this module is to:
- Read real-time water quality parameters  
- Ensure accurate sampling of sensor values  
- Send processed data to the backend (Flask/Node-RED)  
- Maintain reliability even in outdoor pond environments  

---

## 📁 2. Folder Structure

```
hardware/
│
├── firmware/
│   └── esp32_pond_node.ino
│
├── circuits/
│   ├── wiring_diagram.png
│   ├── sensor_connections.pdf
│   └── hardware_block_diagram.png
│
├── components/
│   └── components_list.md
│
└── hardware_documentation.md   ← (this file)
```

---

## ⚙️ 3. Hardware Components Used

1. **ESP32 Microcontroller**  
   - WiFi-enabled  
   - Reads analog/digital sensors  
   - Sends data to Flask/Node-RED  

2. **Sensors**  
   - 🧪 pH Sensor → Measures acidity  
   - 🌫 Turbidity Sensor → Measures water clarity  
   - 💧 TDS Sensor → Measures dissolved salts  
   - 🌡 Temperature Sensor → Temperature 
   - 🏭 MQ135 → Air quality sensor  

3. **Supporting Items**  
   - Breadboard  
   - Jumper wires  
   - 5V/3.3V regulated power supply  
   - Waterproof sensor casing  

See `/hardware/components/components_list.md` for the full list.

---

## 🔌 4. Sensor Wiring Summary

| Sensor | ESP32 Pin | Power | Notes |
|--------|-----------|--------|-------|
| Temperature | GPIO 4 | 3.3V | Temperature |
| pH Sensor | GPIO 34 | 3.3V/5V | Analog input only |
| Turbidity Sensor | GPIO 35 | 5V | Better accuracy at 5V |
| TDS Sensor | GPIO 32 | 3.3V | Must isolate from noise |
| MQ135 | GPIO 33 | 5V | Requires preheating |

Detailed diagrams are available in `circuits/`.

---

## 🔄 5. Working Principle

The ESP32 microcontroller:
1. Reads real-time values from all sensors  
2. Applies basic filtering to avoid noise spikes  
3. Packages data as JSON or form-data  
4. Sends it to the Flask backend using HTTP POST or MQTT  

Back-end server predicts:  
→ **Optimal** or **Non-Optimal pond condition**

---

## 📝 6. ESP32 Code Overview

File: `/hardware/firmware/esp32_pond_node.ino`

The firmware performs:
- Sensor initialization  
- Analog/digital value conversion  
- Calibration for pH & TDS sensors  
- Data formatting  
- Wi-Fi handling  
- Server communication  

---

## 🛡 7. Safety and Installation Notes

- Keep ESP32 and circuits **away from water**  
- Use waterproof sensor probes  
- Turbidity and pH probes must be cleaned periodically  
- For outdoor use, place ESP32 in a sealed box  
- Common ground must be maintained across all sensors  

---

## 📘 8. Conclusion

This hardware layer forms the backbone of the Smart Fish Aquaculture System by collecting reliable real-time water quality metrics.  
It seamlessly integrates with the Machine Learning and Web Dashboard modules to provide a complete monitoring and prediction system.

---
