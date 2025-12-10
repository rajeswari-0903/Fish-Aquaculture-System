#include <WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "ThingSpeak.h"

// WiFi credentials
const char* ssid = "Karthik";
const char* password = "12345678";

// ThingSpeak settings
const char* thingSpeakHost = "api.thingspeak.com";
const unsigned long channelID = 2896310;  // Replace with your channel ID
const char* writeAPIKey = "FLEX2GICTUGZJG8N";         // Replace with your write API key
WiFiClient client;

// DS18B20 Temperature sensor setup
#define ONE_WIRE_BUS 21  // GPIO21
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Analog pins
const int MQ135_PIN = 36;
const int TDS_PIN = 39;
const int PH_PIN = 34;
const int TURBIDITY_PIN = 35;

// Calibration constants
const float R0_MQ135 = 9.8;
const float calibrationFactor_MQ135 = 110.0;
const float exponent_MQ135 = -2.0;

const float TDS_Calibration = 0.5;
const float pH_Voltage_Offset = 0.0;
const float Turbidity_Calibration = -1120.4;
const float Turbidity_Voltage_Offset = 5742.3;

float analogToVoltage(int value) {
  return (float)value * (3.3 / 4095.0);
}

float voltageToPH(float voltage) {
  return 3.5 * voltage + pH_Voltage_Offset;
}

float getResistance(float voltage, float R0) {
  return (3.3 - voltage) / voltage * R0;
}

float calculatePPM(float resistance, float R0, float calFactor, float exponent) {
  float ratio = resistance / R0;
  return calFactor * pow(ratio, exponent);
}

float voltageToTDS(float voltage) {
  return voltage * TDS_Calibration * 1000.0;
}

float voltageToTurbidity(float voltage) {
  return Turbidity_Calibration * voltage + Turbidity_Voltage_Offset;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  sensors.begin();

  WiFi.begin(ssid, password);
  Serial.println("\n🔌 Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi connected!");
  Serial.print("📶 IP: ");
  Serial.println(WiFi.localIP());

  ThingSpeak.begin(client);
}

void loop() {
  // Sensor Readings
  float mq135Voltage = analogToVoltage(analogRead(MQ135_PIN));
  float tdsVoltage = analogToVoltage(analogRead(TDS_PIN));
  float phVoltage = analogToVoltage(analogRead(PH_PIN));
  float turbidityVoltage = analogToVoltage(analogRead(TURBIDITY_PIN));

  float mq135Resistance = getResistance(mq135Voltage, R0_MQ135);
  float airQualityPPM = calculatePPM(mq135Resistance, R0_MQ135, calibrationFactor_MQ135, exponent_MQ135) + 120;
  float tdsPPM = voltageToTDS(tdsVoltage);
  float ph = voltageToPH(phVoltage);
  float turbidityNTU = voltageToTurbidity(turbidityVoltage) - 4770;

  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);

  Serial.printf("Air Quality: %.2f ppm\nTDS: %.2f ppm\npH: %.2f\nTurbidity: %.2f NTU\nTemperature: %.2f°C\n\n",
                airQualityPPM, tdsPPM, ph, turbidityNTU, temperature);

  // Upload to ThingSpeak
  ThingSpeak.setField(1, airQualityPPM);
  ThingSpeak.setField(2, tdsPPM);
  ThingSpeak.setField(3, ph);
  ThingSpeak.setField(4, turbidityNTU);
  ThingSpeak.setField(5, temperature);

  int status = ThingSpeak.writeFields(channelID, writeAPIKey);

  if (status == 200) {
    Serial.println("✅ Data sent to ThingSpeak.");
  } else {
    Serial.print("❌ Failed to send data. Error code: ");
    Serial.println(status);
  }

  delay(15000);  // Delay 10 seconds before next update
}