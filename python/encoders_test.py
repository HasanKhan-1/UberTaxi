
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

# from gpiozero import Button
# from time import sleep

# # Encoder 1 (Left) GPIO Pins
# encoder1PinA = 10  # GPIO Pin 17 (Physical Pin 11)
# encoder1PinB = 9   # GPIO Pin 27 (Physical Pin 13)

# # Encoder 2 (Right) GPIO Pins
# encoder2PinA = 21  # GPIO Pin 22 (Physical Pin 15)
# encoder2PinB = 18  # GPIO Pin 23 (Physical Pin 16)

# # Initialize encoder positions
# encoderPos1 = 0
# encoderPos2 = 0

# # Define callback functions for encoders
# def handle_encoder1A():
#     global encoderPos1
#     if encoder1B.is_pressed:  # If B is HIGH when A changes, moving one direction
#         encoderPos1 += 1
#     else:  # If B is LOW when A changes, moving the other direction
#         encoderPos1 -= 1

# def handle_encoder2A():
#     global encoderPos2
#     if encoder2B.is_pressed:  # If B is HIGH when A changes, moving one direction
#         encoderPos2 += 1
#     else:  # If B is LOW when A changes, moving the other direction
#         encoderPos2 -= 1

# # Setup gpiozero Buttons with pull-ups and debouncing
# encoder1A = Button(encoder1PinA, pull_up=True, bounce_time=0.001)
# encoder1B = Button(encoder1PinB, pull_up=True, bounce_time=0.001)

# encoder2A = Button(encoder2PinA, pull_up=True, bounce_time=0.001)
# encoder2B = Button(encoder2PinB, pull_up=True, bounce_time=0.001)

# # Attach the event handlers **only to channel A**
# encoder1A.when_pressed = handle_encoder1A
# encoder2A.when_pressed = handle_encoder2A

# try:
#     while True:
#         # Print the encoder positions, scaling them
#         print("Encoder 1 (Left): {:.2f} | Encoder 2 (Right): {:.2f}".format(
#             encoderPos1 * (210.48666 / (12 * 34 * 2.36)),
#             encoderPos2 * (210.48666 / (12 * 34 * 2.36))
#         ))
#         sleep(0.1)

# except KeyboardInterrupt:
#     print("Program interrupted")


from gpiozero import RotaryEncoder
from signal import pause

# Define encoder objects
encoder1 = RotaryEncoder(a=20, b=21, max_steps=0)  # Left Encoder
encoder2 = RotaryEncoder(a=10, b=9, max_steps=0)  # Right Encoder

def update_encoders():
    print(f"Left Encoder: {encoder1.steps}, Right Encoder: {encoder2.steps}")

# Monitor encoder values
encoder1.when_rotated = update_encoders
encoder2.when_rotated = update_encoders

print("Encoders are running... Press Ctrl+C to exit.")
pause()


# from gpiozero import DigitalInputDevice
# from time import sleep

# # Check each pin state
# encoder1A = DigitalInputDevice(20)
# encoder1B = DigitalInputDevice(21)
# encoder2A = DigitalInputDevice(10)
# encoder2B = DigitalInputDevice(9)


# print("Monitoring encoder signals... Move the motors and observe changes.")

# try:
#     while True:
#         print(f"Enc1A: {encoder1A.value}, Enc1B: {encoder1B.value}, Enc2A: {encoder2A.value}, Enc2B: {encoder2B.value}")
#         sleep(0.1)
# except KeyboardInterrupt:
#     print("\nStopped.")
