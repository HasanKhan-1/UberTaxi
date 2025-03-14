//#include <Wire.h>
//
//const int SDA_Pin = 20;
//const int SCL_Pin = 21;
//const int ledPin = 13; // *** Change LED Pin here
//
//int LED_Byte = 0;
// 
//void setup() {
//  // Arduino joins I2C bus as slave with address 8
//  Wire.begin(0x8);
//  
//  // Call receiveEvent function when data received                
//  Wire.onReceive(receiveEvent);
//  
//  // Setup pin 13 as output and turn LED off at the beginning
//  pinMode(ledPin, OUTPUT);
//  digitalWrite(ledPin, LOW);
//
//  // Turn off 20k-50k ohm built-in pull up resistors at pins specified
//  digitalWrite(SDA_Pin, LOW);
//  digitalWrite(SCL_Pin, LOW);
//}
// 
//// Function that executes whenever data is received from master device, the Pi 5
//void receiveEvent(int howMany) {
//  LED_Byte = Wire.read(); // receive byte as an integer
//  digitalWrite(ledPin, LED_Byte); // turn on/off LED based on byte information
//  Serial.println(LED_Byte);
//  
//}
//
//void loop() {
//  delay(100); // Keep waiting for data
//}
//
//

#include <Arduino.h>
#include <Wire.h>

// Motor control pins
int IN1 = 4;
int IN2 = 5;
int ENAf = 2; // PWM pin for motor speed control
int ENAr = 3; // PWM pin for motor speed control

int IN3 = 6;
int IN4 = 7;
int ENBf = 8; // PWM pin for motor speed control
int ENBr = 9; // PWM pin for motor speed control

void receiveEvent(int howMany);                                 

void setup() {
  // Initialize I2C communication as a slave
  Wire.begin(0x08); // I2C address must match the one in the Python script
  Wire.onReceive(receiveEvent); // Register event handler for receiving data

  // Set the direction control pins as OUTPUT
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  
  // Set the ENA pin as OUTPUT (to control motor speed)
  pinMode(ENAf, OUTPUT);
  pinMode(ENAr, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  
  // Set the ENA pin as OUTPUT (to control motor speed)
  pinMode(ENBf, OUTPUT);
  pinMode(ENBr, OUTPUT);
}

void loop() {
  // Main loop does nothing, motor control is handled in receiveEvent
}

void receiveEvent(int howMany) {
  if (Wire.available()) {
    int command = Wire.read(); // Read the command sent from the Python script

    switch (command) {
      case 0: // Stop
        analogWrite(ENAf, 0);
        analogWrite(ENAr, 0);
        analogWrite(ENBf, 0);
        analogWrite(ENBr, 0);
        break;
      case 1: // Move forward
        analogWrite(ENAf, 128); // Set speed to 50%
        analogWrite(ENAr, 128);
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);

        analogWrite(ENBf, 128); // Set speed to 50%
        analogWrite(ENBr, 128);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;
      case 2: // Turn left
        analogWrite(ENAf, 128); // Set speed to 50%
        analogWrite(ENAr, 128);
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);

        analogWrite(ENBf, 128); // Set speed to 50%
        analogWrite(ENBr, 128);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;
      case 3: // Turn right
        analogWrite(ENAf, 128); // Set speed to 50%
        analogWrite(ENAr, 128);
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);

        analogWrite(ENBf, 128); // Set speed to 50%
        analogWrite(ENBr, 128);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;
    }
  }
}