#include <Arduino.h>
#include <Wire.h>

// Motor control pins
const int IN1 = 8;  // Input 1 for Motor A
const int IN2 = 7;  // Input 2 for Motor A
const int ENA = 9;  // Enable pin for Motor A (PWM capable)

// Forward declaration of the handleMotorCommand function
void handleMotorCommand(int command);

// I2C event handler: called when data is received from Raspberry Pi
void receiveEvent(int howMany) {
    if (Wire.available()) {
        int command = Wire.read(); // Read the command sent from the Python script
        Serial.print("Received command: ");
        Serial.println(command); // Debugging output
        handleMotorCommand(command); // Call function to control motors
    }
}

void setup() {
    Wire.begin(0x08); // Initialize I2C communication as a slave
    Wire.onReceive(receiveEvent); // Register event handler for receiving data
    Serial.begin(9600); // Start serial monitor for debugging

    // Set motor pins as outputs
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENA, OUTPUT);

    // Stop the motor initially
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);
}

void loop() {
    // Main loop does nothing, motor control is handled in receiveEvent
}

void handleMotorCommand(int command) {
    switch (command) {
        case 0: // Stop
            Serial.println("Command: Stop");
            analogWrite(ENA, 0);
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            break;

        case 1: // Move forward
            Serial.println("Command: Move forward");
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            analogWrite(ENA, 200); // Set speed to 200 (0-255)
            break;

        case 2: // Turn left (stop motor)
            Serial.println("Command: Turn left");
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            analogWrite(ENA, 0);
            break;

        case 3: // Turn right (stop motor)
            Serial.println("Command: Turn right");
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            analogWrite(ENA, 0);
            break;
    }
}