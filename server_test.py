from gpiozero import AngularServo
from time import sleep

servo = AngularServo(14, min_angle=0, max_angle = 180, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)

def set_angle(angle):
    servo.angle = angle
    sleep(1)

try:
    while True:
        set_angle(angle=90)
except KeyboardInterrupt:
    print("servo stopped")