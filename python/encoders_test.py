
# from gpiozero import Button
# from signal import pause
# import time

# # Encoder 1 (Left) GPIO Pins
# encoder1PinA = 17  # GPIO17
# encoder1PinB = 8  # GPIO22

# # Initialize encoder position
# encoderPos1 = 0

# # Define the callback function for encoder 1
# def handle_encoder1A():
#     global encoderPos1
#     if encoder1A.is_pressed == encoder1B.is_pressed:
#         encoderPos1 += 1
#     else:
#         encoderPos1 -= 1

# # Set up the encoder using gpiozero
# encoder1A = Button(encoder1PinA, pull_up=True, bounce_time=0.001)
# encoder1B = Button(encoder1PinB, pull_up=True, bounce_time=0.001)

# # Attach the event handler
# encoder1A.when_pressed = handle_encoder1A
# encoder1A.when_released = handle_encoder1A

# # Run continuously
# try:
#     while True:
#         print("Encoder 1 (Left): {:.2f}".format(
#             encoderPos1 * (210.48666 / (12 * 34 * 2.36))
#         ))
#         time.sleep(0.1)

# except KeyboardInterrupt:
#     print("Program interrupted")

from gpiozero import RotaryEncoder, Button
from time import sleep

# Encoder 1 (Left) GPIO Pins
encoder1PinA = 10  # GPIO Pin 17 (Physical Pin 11)
encoder1PinB = 9  # GPIO Pin 27 (Physical Pin 13)

# Encoder 2 (Right) GPIO Pins
encoder2PinA = 21  # GPIO Pin 22 (Physical Pin 15)
encoder2PinB = 18  # GPIO Pin 23 (Physical Pin 16)

# Initialize encoder positions
encoderPos1 = 0
encoderPos2 = 0

# Create RotaryEncoder objects
encoder1 = RotaryEncoder(encoder1PinA, encoder1PinB, wrap=False)
encoder2 = RotaryEncoder(encoder2PinA, encoder2PinB, wrap=False)

# Define the callback functions for encoders
def handle_encoder1():
    global encoderPos1
    encoderPos1 = encoder1.steps

def handle_encoder2():
    global encoderPos2
    encoderPos2 = encoder2.steps

# Attach the event handlers
encoder1.when_rotated = handle_encoder1
encoder2.when_rotated = handle_encoder2

try:
    while True:
        # Print the encoder positions, scaling them
        print("Encoder 1 (Left): {:.2f} | Encoder 2 (Right): {:.2f}".format(
            encoderPos1 * (210.48666 / (12 * 34 * 2.36)),
            encoderPos2 * (210.48666 / (12 * 34 * 2.36))
        ))
        sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # No need for explicit cleanup with gpiozero
    pass
