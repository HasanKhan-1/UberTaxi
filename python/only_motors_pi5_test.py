# from gpiozero import PWMOutputDevice, DigitalOutputDevice
# from time import sleep


# IN1 = DigitalOutputDevice(14)
# IN2 = DigitalOutputDevice(5)
# IN3 = DigitalOutputDevice(2)
# IN4 = DigitalOutputDevice(3)
# ENA = PWMOutputDevice(4)  # Speed control (PWM)

# ENB = PWMOutputDevice(23)  # Speed control (PWM)

# ENAb = PWMOutputDevice(27)  # Speed control (PWM)
# ENBb = PWMOutputDevice(24)  # Speed control (PWM)

# # Setup PWM for speed control
# ENA.value = 0.5  # 50% speed
# ENB.value = 0.5
# ENAb.value = 0.5  # 50% speed
# ENBb.value = 0.5


# def move_forward():
#     """Move both motors forward."""
#     print("Moving forward")
#     IN1.off()
#     IN2.on()
#     IN3.on()
#     IN4.off()
#     ENA.value = 1
#     ENB.value = 1
#     ENAb.value = 1
#     ENBb.value = 1

# def move_backward():
#     """Move both motors backward."""
#     print("Moving backward")
#     IN1.on()
#     IN2.off()
#     IN3.on()
#     IN4.off()
#     ENA.value = 0.5
#     ENB.value = 0.5
#     ENAb.value = 0.5
#     ENBb.value = 0.5

# def stop_motors():
#     """Stop both motors."""
#     print("Stopping motors")
#     IN1.off()
#     IN2.off()
#     IN3.off()
#     IN4.off()
#     ENA.off()
#     ENB.off()
#     ENAb.off()
#     ENBb.off()

# if __name__ == "__main__":
#     while True:
#         move_forward()
#         # sleep(2)  # Move forward for 2 seconds
#         # stop_motors()
#         # sleep(1)  # Stop for 1 second
#         # move_backward()
#         # sleep(2)  # Move backward for 2 seconds
#         # stop_motors()
#     # except KeyboardInterrupt:
#     #     pass
#     # finally:
#     #     stop_motors()

from gpiozero import RotaryEncoder, PWMOutputDevice, DigitalOutputDevice
from time import sleep

# Define encoder objects
encoder1 = RotaryEncoder(a=20, b=21, max_steps=0)  # Left Encoder
encoder2 = RotaryEncoder(a=10, b=9, max_steps=0)  # Right Encoder

# Define motor control pins
IN1 = DigitalOutputDevice(14)
IN2 = DigitalOutputDevice(5)
IN3 = DigitalOutputDevice(2)
IN4 = DigitalOutputDevice(3)
ENA = PWMOutputDevice(4)  
ENB = PWMOutputDevice(23)
ENAb = PWMOutputDevice(27)
ENBb = PWMOutputDevice(24)

# Target encoder count
TARGET_STEPS = 1000

def move_forward():
    """Move both motors forward."""
    print("Moving forward")
    IN1.off()
    IN2.on()
    IN3.on()
    IN4.off()
    ENA.value = 1
    ENB.value = 1
    ENAb.value = 1
    ENBb.value = 1

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

def update_encoders():
    """Check encoder steps and stop when reaching the target."""
    print(f"Left Encoder: {encoder1.steps}, Right Encoder: {encoder2.steps}")

    if abs(encoder1.steps) >= TARGET_STEPS and abs(encoder2.steps) >= TARGET_STEPS:
        stop_motors()
        print("Target reached")
        exit()  # Stops the script

# Attach encoder event listeners
encoder1.when_rotated = update_encoders
encoder2.when_rotated = update_encoders

# Start moving
move_forward()

# Keep script running
while True:
    sleep(0.1)
