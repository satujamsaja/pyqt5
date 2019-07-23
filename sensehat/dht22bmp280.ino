/***
 * DHT22 and BMP280
 */

// Include libraries.
#include "DHT.h"
#include "Adafruit_BMP280.h"

// DHT22 pin data input Pin 2 digital.
#define DHTPIN 2

// DHT sensor type.
#define DHTTYPE DHT22

// Change to your location sea level pressure (Nusa Dua, Bali, Indonesia).
#define SEALEVEL_PRESSURE 1014

// Init sensor.
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(115200);

  // Sensor initialization.
  dht.begin();
  if (!bmp.begin()) {
    Serial.println("Could not find BMP280 sensor. Check wiring or I2C address!");
  }
}

void loop() {
  // set delay reading (2 seconds)
  delay(1000);

  // Read sensor data.  
  float humidity = dht.readHumidity();
  float tempC = dht.readTemperature();

  // Read sensor.
  float p = bmp.readPressure() / 100;  // Converted to mb, 1mb = 100hPa
  float t = bmp.readTemperature();
  float a = bmp.readAltitude(SEALEVEL_PRESSURE);

  // Print data to serial.
  Serial.print(tempC);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.print(p);
  Serial.println("");
}
