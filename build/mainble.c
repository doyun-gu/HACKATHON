#include "motor_control.h"
#include "servo_control.h"
#include "BLE_control.h"

#include <SoftwareSerial.h>

char receivedChar = '\0';

void setup() {
  Serial.begin(9600); 
  BLEModule.begin(9600);
  SoftwareSerial BLEModule (9, 8);
  Serial.println("BLE Communication Started. Waiting for DATA...");
  // set up Serial library at 9600 bps
  
  //turn on motor
  motor1.setSpeed(0);
  motor1.run(RELEASE);
  motor2.setSpeed(0);
  motor2.run(RELEASE);
  motor3.setSpeed(0);
  motor3.run(RELEASE);
  motor4.setSpeed(0);
  motor4.run(RELEASE);

  myservo.attach(10);

  
}

void newDataReceived(){

  switch(receivedChar){
    case 'w':
      motors_forward();
    break;
    case 's':
       motors_backward();
    break;
    case 'a':
       motors_left();
    break;
    case 'd':
      motors_right();
    break;
  }
} 

void loop() {
  uint8_t i;
  
//  if (BLEModule.available()) { // Check if there is data from Bluetooth
//    receivedChar = BLEModule.read(); // Read the character
//    Serial.print("Received: ");
//    Serial.println(receivedChar); // Print to the hardware serial
//  }

  if(Serial.available()){
    receivedChar = Serial.read();
    Serial.print("Received: ");
    Serial.println(receivedChar);
    newDataReceived();
  }
}