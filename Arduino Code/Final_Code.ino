#include <WiFi.h>
#include <HTTPClient.h>
#include "HX711.h"
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "A34 5G";
const char* password = "shlok098";

// Firebase Realtime Database URL (Base)
const char* firebaseBaseUrl = "https://tkph-ace70-default-rtdb.firebaseio.com/trucks/truck1/readings/.json";

// HX711 Load Cell Connections
#define DT 21
#define SCK 22
HX711 scale;

// Hall Effect Sensor (Speed Measurement)
#define HALL_SENSOR_PIN 23
volatile int revolutionCount = 0;
unsigned long lastTime = 0;

// Function prototypes
float getStableWeight();
void sendToFirebase(float weight_tonnes, float speed, float tkph);
void IRAM_ATTR countRevolution() {
    revolutionCount++;
}

void setup() {
    Serial.begin(115200);
    
    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Load Cell Setup
    scale.begin(DT, SCK);
    scale.set_scale(10000.0); // Update after calibration
    scale.tare();  

    // Hall Sensor Setup
    pinMode(HALL_SENSOR_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(HALL_SENSOR_PIN), countRevolution, FALLING);
}

void loop() {
    // Get weight reading
    float weight_kg = getStableWeight();
    float weight_tonnes = weight_kg / 1000.0; // Convert to tonnes

    Serial.print("Weight (tonnes): ");
    Serial.println(weight_tonnes);

    // Calculate Speed
    unsigned long currentTime = millis();
    float speed = (revolutionCount * 2.5) / ((currentTime - lastTime) / 1000.0);
    Serial.print("Speed (km/h): ");
    Serial.println(speed);
    revolutionCount = 0;
    lastTime = currentTime;

    // Calculate TKPH
    float tkph = weight_tonnes * speed;
    Serial.print("TKPH: ");
    Serial.println(tkph);

    // Send data to Firebase
    sendToFirebase(weight_tonnes, speed, tkph);

    delay(3000); // Send data every 5 seconds
}


// Function to send data to Firebase
// Global Entry Counter
int entryNumber = 1;  // Start from 1

void sendToFirebase(float weight_tonnes, float speed, float tkph) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        // Use entryNumber instead of millis() in the Firebase path
        String path = "https://tkph-ace70-default-rtdb.firebaseio.com/trucks/truck1/readings/" + 
                      String(entryNumber) + ".json";

        http.begin(path);
        http.addHeader("Content-Type", "application/json");

        // JSON Payload
        StaticJsonDocument<200> doc;
        doc["entry_no"] = entryNumber;  // Store the entry number
        doc["truck_id"] = 1;
        doc["tkph"] = tkph;
        doc["speed"] = speed;
        doc["payload"] = weight_tonnes;

        String jsonPayload;
        serializeJson(doc, jsonPayload);

        Serial.println("Sending data to Firebase...");
        Serial.println(jsonPayload);

        // Send HTTP PUT request
        int httpResponseCode = http.PUT(jsonPayload);

        if (httpResponseCode > 0) {
            Serial.println("Data sent to Firebase successfully");
            Serial.print("HTTP Response code: ");
            Serial.println(httpResponseCode);

            entryNumber++; // Increment the entry number only on successful upload
        } else {
            Serial.print("Error sending data. HTTP Response code: ");
            Serial.println(httpResponseCode);
            Serial.println(http.errorToString(httpResponseCode));
        }

        http.end();
    } else {
        Serial.println("WiFi Disconnected");
    }
}


// Function to get stable weight
float getStableWeight() {
    float sum = 0;
    int readings = 10;

    for (int i = 0; i < readings; i++) {
        float reading = scale.get_units();
        if (isnan(reading)) {
            Serial.println("Error: HX711 reading invalid!");
            return 0; // Avoid sending invalid data
        }
        sum += reading;
        delay(10);
    }

    float avg_weight = sum / readings;
    return avg_weight < 0 ? -avg_weight : avg_weight; // Fix negative values
}