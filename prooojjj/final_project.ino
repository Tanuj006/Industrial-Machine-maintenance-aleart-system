#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11 // DHT 11

DHT dht(DHTPIN, DHTTYPE);
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

void setup() {
  Serial.begin(9600);
  if (!accel.begin()) {
    Serial.println("No ADXL345 detected!");
    while (1);
  }
  dht.begin();
}

void loop() {
  sensors_event_t event; 
  accel.getEvent(&event);
  
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  
  Serial.print("X: "); Serial.print(event.acceleration.x); Serial.print(", ");
  Serial.print("Y: "); Serial.print(event.acceleration.y); Serial.print(", ");
  Serial.print("Z: "); Serial.print(event.acceleration.z); Serial.print(", ");
  Serial.print("Temperature: "); Serial.print(temperature); Serial.print(", ");
  Serial.print("Humidity: "); Serial.print(humidity);
  Serial.println();

  delay(2000);  // Adjust delay as needed
}

