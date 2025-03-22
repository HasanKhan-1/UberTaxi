from gpiozero import Servo, AngularServo
from time import sleep

# servo = Servo(16)
servo = AngularServo(16, min_angle=-90, max_angle=90)

while True:
    servo.angle = 0
    sleep(2)
    servo.angle = 45
    sleep(2)
    servo.angle = 90
    sleep(2)

