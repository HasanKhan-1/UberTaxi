from gpiozero import AngularServo
from time import sleep

# Create an AngularServo object
servo = AngularServo(26, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)

try:
    while True:
        servo.angle = -90  # Move to -90 degrees
        sleep(1)
        servo.angle = 0    # Move to 0 degrees (center)
        sleep(1)
        servo.angle = 90   # Move to 90 degrees
        sleep(1)
except KeyboardInterrupt:
    servo.close()
