from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep

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


def move_forward():
    """Move both motors forward."""
    print("Moving forward")
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    ENA.value = 0.5
    ENB.value = 0.5
    ENAb.value = 0.5
    ENBb.value = 0.5

def move_backward():
    """Move both motors backward."""
    print("Moving backward")
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    ENA.value = 0.5
    ENB.value = 0.5
    ENAb.value = 0.5
    ENBb.value = 0.5

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

if __name__ == "__main__":
    while True:
        move_forward()
        sleep(2)  # Move forward for 2 seconds
        stop_motors()
        sleep(1)  # Stop for 1 second
        move_backward()
        sleep(2)  # Move backward for 2 seconds
        stop_motors()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     stop_motors()