#Just a file for testing the basic movement of either motors on the robot
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

# Motor Pins
IN1 = DigitalOutputDevice(17)
IN2 = DigitalOutputDevice(18)
IN3 = DigitalOutputDevice(22)
IN4 = DigitalOutputDevice(23)
ENA = PWMOutputDevice(24)  # Speed control (PWM)
ENB = PWMOutputDevice(25)  # Speed control (PWM)

# Setup PWM for speed control
ENA.value = 0.5  # 50% speed
ENB.value = 0.5

# Move both motors forward
IN1.on()
IN2.off()
IN3.on()
IN4.off()

sleep(2)

# Stop motors
IN1.off()
IN2.off()
IN3.off()
IN4.off()

sleep(1)

# Move both motors backward
IN1.off()
IN2.on()
IN3.off()
IN4.on()

sleep(2)

# Stop motors
IN1.off()
IN2.off()
IN3.off()
IN4.off()

ENA.off()
ENB.off()