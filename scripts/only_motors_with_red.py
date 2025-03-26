import RPi.GPIO as GPIO
import cv2
import numpy as np
import time

class MotorController:
    def __init__(self):
        # Motor Pins
        self.in1 = 6
        self.in2 = 5
        self.in3 = 22
        self.in4 = 27

        self.en1 = 16  # Forward speed control
        self.en2 = 17  # Forward speed control
        self.en1b = 26  # Backward speed control
        self.en2b = 23  # Backward speed control

        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set up GPIO pins
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        GPIO.setup(self.en1, GPIO.OUT)
        GPIO.setup(self.en2, GPIO.OUT)

        # Initialize PWM for speed control
        self.pwm1 = GPIO.PWM(self.en1, 100)  # 100 Hz frequency
        self.pwm2 = GPIO.PWM(self.en2, 100)  # 100 Hz frequency

        # Start PWM with 0% duty cycle (motors stopped)
        self.pwm1.start(0)
        self.pwm2.start(0)

    def stop_motors(self):
        """Stop all motors."""
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(0)

    def move_forward(self, speed):
        """Move both motors forward."""
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(speed)

    def move_left(self, speedright, speedleft):
        """Turn left by adjusting motor speeds."""
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.pwm1.ChangeDutyCycle(speedright)
        self.pwm2.ChangeDutyCycle(speedleft)

    def move_right(self, speedright, speedleft):
        """Turn right by adjusting motor speeds."""
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.HIGH)
        GPIO.output(self.in4, GPIO.LOW)
        self.pwm1.ChangeDutyCycle(speedright)
        self.pwm2.ChangeDutyCycle(speedleft)

    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop_motors()
        GPIO.cleanup()