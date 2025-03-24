#include <Arduino.h>
#include <Wire.h>
#include <PinChangeInterrupt.h>

// Encoder 1 (Left) - INT1
volatile int encoderPos1 = 0;
const int encoder1PinA = 3;
const int encoder1PinB = 2;

// Encoder 2 (Right) - PCI
volatile int encoderPos2 = 0;
const int encoder2PinA = 4;
const int encoder2PinB = 5;

void setup() {
  // Encoder 1
  pinMode(encoder1PinA, INPUT);
  pinMode(encoder1PinB, INPUT);
  attachInterrupt(digitalPinToInterrupt(encoder1PinA), handleEncoder1A, CHANGE);

  // Encoder 2
  pinMode(encoder2PinA, INPUT);
  pinMode(encoder2PinB, INPUT);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(encoder2PinA), handleEncoder2A, CHANGE);

  Serial.begin(9600);

  // Initialize I2C communication as a slave
  Wire.begin(0x08);
  Wire.onRequest(requestEvent);
}

void loop() {
  // Main loop does nothing, encoder values are sent in requestEvent
}

// Interrupt for Encoder 1
void handleEncoder1A() {
  if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
    encoderPos1++;
  } else {
    encoderPos1--;
  }
}

// Pin change interrupt for Encoder 2
void handleEncoder2A() {
  if (digitalRead(encoder2PinA) == digitalRead(encoder2PinB)) {
    encoderPos2++;
  } else {
    encoderPos2--;
  }
}

// I2C request event handler
void requestEvent() {
  Wire.write((byte*)&encoderPos1, sizeof(encoderPos1));
  Wire.write((byte*)&encoderPos2, sizeof(encoderPos2));
}