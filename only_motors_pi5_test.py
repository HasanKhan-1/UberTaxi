from gpiozero import OutputDevice, PWMOutputDevice
import cv2
import numpy as np
import time

# Motor control pins
in1 = 6
in2 = 5
in3 = 25
in4 = 24

# PWM speed control pins
ena_top = 26   # Forward speed control
ena_bottom = 16  # Forward speed control
enb_top = 23  # Backward speed control
enb_bottom = 22  # Backward speed control

# Initialize motor control pins
motor_in1 = OutputDevice(in1)
motor_in2 = OutputDevice(in2)
motor_in3 = OutputDevice(in3)
motor_in4 = OutputDevice(in4)

# Initialize PWM for speed control
pwm_ena_top = PWMOutputDevice(ena_top, initial_value=0)
pwm_ena_bottom = PWMOutputDevice(ena_bottom, initial_value=0)
pwm_enb_top = PWMOutputDevice(enb_top, initial_value=0)
pwm_enb_bottom = PWMOutputDevice(enb_bottom, initial_value=0)

def stop_motors():
    motor_in1.off()
    motor_in2.off()
    motor_in3.off()
    motor_in4.off()
    pwm_ena_top.value = 0
    pwm_ena_bottom.value = 0
    pwm_enb_top.value = 0
    pwm_enb_bottom.value = 0

def move_forward(speed):
    motor_in1.on()
    motor_in2.off()
    motor_in3.on()
    motor_in4.off()
    pwm_ena_top.value = speed / 100
    pwm_ena_bottom.value = speed / 100

def move_spin(speed):
    motor_in1.off()
    motor_in2.on()
    motor_in3.on()
    motor_in4.off()
    pwm_ena_top.value = speed / 100
    pwm_ena_bottom.value = speed / 100

def move_backwards(speed):
    motor_in1.off()
    motor_in2.on()
    motor_in3.off()
    motor_in4.on()
    pwm_enb_top.value = speed / 100
    pwm_enb_bottom.value = speed / 100

if __name__ == "__main__":
        stop_motors()
        time.sleep(5)
        move_forward(50)  # Move forward with 100% speed
