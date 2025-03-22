from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep
import cv2
import numpy as np
import time
from pid_controller import PID  # Import the PID controller

# Motor Pins
IN1 = DigitalOutputDevice(6)
IN2 = DigitalOutputDevice(5)
IN3 = DigitalOutputDevice(25)
IN4 = DigitalOutputDevice(24)
ENA = PWMOutputDevice(17)  # Speed control (PWM)
ENB = PWMOutputDevice(22)  # Speed control (PWM)

ENAb = PWMOutputDevice(27)  # Speed control (PWM)
ENBb = PWMOutputDevice(23)  # Speed control (PWM)

# Setup PWM for speed control
ENA.value = 0.5  # 50% speed
ENB.value = 0.5
ENAb.value = 0.5  # 50% speed
ENBb.value = 0.5

# Initialize PID controller
pid = PID(Kp=0.1, Ki=0.01, Kd=0.05)
setpoint = 80  # Desired position (center of the frame)

def move_forward(speed):
    """Move both motors forward with a given speed."""
    print("Moving forward")
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    ENA.value = speed
    ENB.value = speed
    ENAb.value = speed
    ENBb.value = speed

def move_backward(speed):
    """Move both motors backward with a given speed."""
    print("Moving backward")
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    ENA.value = speed
    ENB.value = speed
    ENAb.value = speed
    ENBb.value = speed

def stop_motors():
    """Stop both motors."""
    print("Stopping motors")
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    ENA.off()
    ENB.off()
    ENAb.off()
    ENBb.off()

def move_spin(speed):
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    ENA.value = speed
    ENB.value = speed
    ENAb.value = speed
    ENBb.value = speed