import cv2
import numpy as np
import time
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from simple_pid import PID  # Import the PID controller


class MotorController:
    def __init__(self):
        """Initialize motor pins and PWM."""
        # Motor Pins
        self.IN1 = DigitalOutputDevice(5)
        self.IN2 = DigitalOutputDevice(14)
        self.IN3 = DigitalOutputDevice(2)
        self.IN4 = DigitalOutputDevice(3)
        self.ENA = PWMOutputDevice(4)  # Speed control (PWM)
        self.ENB = PWMOutputDevice(23)  # Speed control (PWM)
        self.ENAb = PWMOutputDevice(27)  # Speed control (PWM)
        self.ENBb = PWMOutputDevice(24)  # Speed control (PWM)

        # Set initial speed to 50%
        self.ENA.value = 0.5
        self.ENB.value = 0.5
        self.ENAb.value = 0.5
        self.ENBb.value = 0.5

    def move_forward(self, speed):
        """Move both motors forward with a given speed."""
        print("Moving forward")
        self.IN1.on()
        self.IN2.off()
        self.IN3.on()
        self.IN4.off()
        self._set_speed(speed)

    def move_backward(self, speed):
        """Move both motors backward with a given speed."""
        print("Moving backward")
        self.IN1.off()
        self.IN2.on()
        self.IN3.off()
        self.IN4.on()
        self._set_speed(speed)

    def move_spin(self, speed):
        """Spin the robot in place."""
        print("Spinning")
        self.IN1.off()
        self.IN2.on()
        self.IN3.off()
        self.IN4.on()
        self._set_speed(speed)

    def stop_motors(self):
        """Stop all motors."""
        print("Stopping motors")
        self.IN1.off()
        self.IN2.off()
        self.IN3.off()
        self.IN4.off()
        self._set_speed(0)

    def _set_speed(self, speed):
        """Set the speed for all motors."""
        self.ENA.value = speed
        self.ENB.value = speed
        self.ENAb.value = speed
        self.ENBb.value = speed

