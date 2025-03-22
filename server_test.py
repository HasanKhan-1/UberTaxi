from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = AngularServo(
    26,  # GPIO26
    min_pulse_width=0.0005,  # 0.5ms pulse for 0°
    max_pulse_width=0.0024,  # 2.4ms pulse for 180°
    pin_factory=factory
)

servo.angle = 90  # Set to 90°
