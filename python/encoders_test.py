import RPi.GPIO as GPIO
import time

# Encoder 1 (Left) GPIO Pins
encoder1PinA = 10  # GPIO Pin 17 (Physical Pin 11)
encoder1PinB = 9  # GPIO Pin 27 (Physical Pin 13)

# Encoder 2 (Right) GPIO Pins
encoder2PinA = 21  # GPIO Pin 22 (Physical Pin 15)
encoder2PinB = 18  # GPIO Pin 23 (Physical Pin 16)

# Initialize encoder positions
encoderPos1 = 0
encoderPos2 = 0

# Setup the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use Broadcom GPIO pin numbering
GPIO.setwarnings(False)  # Disable GPIO warnings

# Set up Encoder 1 pins
GPIO.setup(encoder1PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder1PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up Encoder 2 pins
GPIO.setup(encoder2PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder2PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the callback functions for interrupts
def handle_encoder1A(channel):
    """Callback function for Encoder 1."""
    global encoderPos1
    if GPIO.input(encoder1PinA) == GPIO.input(encoder1PinB):
        encoderPos1 += 1
    else:
        encoderPos1 -= 1

def handle_encoder2A(channel):
    """Callback function for Encoder 2."""
    global encoderPos2
    if GPIO.input(encoder2PinA) == GPIO.input(encoder2PinB):
        encoderPos2 += 1
    else:
        encoderPos2 -= 1

# Set up interrupts for both encoders
GPIO.add_event_detect(encoder1PinA, GPIO.BOTH, callback=handle_encoder1A, bouncetime=1)
GPIO.add_event_detect(encoder2PinA, GPIO.BOTH, callback=handle_encoder2A, bouncetime=1)

try:
    while True:
        # Print the encoder positions, scaling them
        print("Encoder 1 (Left): {:.2f} | Encoder 2 (Right): {:.2f}".format(
            encoderPos1 * (210.48666 / (12 * 34 * 2.36)),
            encoderPos2 * (210.48666 / (12 * 34 * 2.36))
        ))
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()  # Clean up GPIO settings


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
