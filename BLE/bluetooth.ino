// Code for arduino and bluetooth module
// Az-Delivery Board with ESP32 and Bluetooth Module

void setup() {
    Serial.begin(115200);
    pinMode(4, OUTPUT);
    digitalWrite(4, LOW);

    // Set RX and TX pins
    Serial2.begin(9600, SERIAL_8N1, 16, 17);
    
}