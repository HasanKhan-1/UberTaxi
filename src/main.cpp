#include <Arduino.h>
#include <Wire.h>

// Motor control pins
const int IN1 = 8;  // Input 1 for Left Motor
const int IN2 = 7;  // Input 2 for Left Motor
const int ENA = 9;  // Enable pin for Motor A (PWM capable)
const int IN3 = 6;  // Input 1 for Right Motor
const int IN4 = 5;  // Input 2 for Right Motor
const int ENB = 4;  // Enable pin for Motor B (PWM capable)

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
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(ENB, OUTPUT);

    // Stop the motor initially
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    analogWrite(ENA, 0);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, 0);
}

void loop() {
    // Main loop does nothing, motor control is handled in receiveEvent
}

void handleMotorCommand(int command) {
    switch (command) {
        case 0: // Stop
            Serial.println("Command: Stop");
            analogWrite(ENA, 0);
            analogWrite(ENB, 0);
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, LOW);
            digitalWrite(IN4, LOW); 
            break;

        case 1: // Move forward (A&B)
            Serial.println("Command: Move forward");
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, HIGH);
            digitalWrite(IN4, LOW);
            analogWrite(ENA, 200); // Set speed to 200 (0-255)
            analogWrite(ENB, 200); // Set speed to 200 (0-255)
            break;
        case 2: // Turn left (A stop, B forward)
            Serial.println("Command: Turn left");
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, HIGH);
            digitalWrite(IN4, LOW);
            analogWrite(ENA, 0); // Stop left motor
            analogWrite(ENB, 200); // Set speed to 200 (0-255)
            break;
        case 3: // Turn right (B stop, A forward)
            Serial.println("Command: Turn right");
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, LOW);
            digitalWrite(IN4, LOW);
            analogWrite(ENA, 200); // Set speed to 200 (0-255)
            analogWrite(ENB, 0); // Stop right motor
            break;
    }
}