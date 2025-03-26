from gpiozero import DigitalOutputDevice

# ENCODER1 = DigitalOutputDevice(6)

import RPi.GPIO as GPIO
import time

# Encoder 1 (Left) GPIO Pins
encoder1PinA = 17  # GPIO Pin 17 (Physical Pin 11)
encoder1PinB = 22  # GPIO Pin 27 (Physical Pin 13)

# Encoder 2 (Right) GPIO Pins
# encoder2PinA = 22  # GPIO Pin 22 (Physical Pin 15)
# encoder2PinB = 23  # GPIO Pin 23 (Physical Pin 16)

# Initialize encoder positions
encoderPos1 = 0
# encoderPos2 = 0

# Setup the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up Encoder 1 pins
GPIO.setup(encoder1PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder1PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up Encoder 2 pins
# GPIO.setup(encoder2PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(encoder2PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define the callback functions for interrupts
def handle_encoder1A(channel):
    global encoderPos1
    if GPIO.input(encoder1PinA) == GPIO.input(encoder1PinB):
        encoderPos1 += 1
    else:
        encoderPos1 -= 1

# def handle_encoder2A(channel):
#     global encoderPos2
#     if GPIO.input(encoder2PinA) == GPIO.input(encoder2PinB):
#         encoderPos2 += 1
#     else:
#         encoderPos2 -= 1

# Set up interrupts for both encoders
GPIO.add_event_detect(encoder1PinA, GPIO.BOTH, callback=handle_encoder1A)
# GPIO.add_event_detect(encoder2PinA, GPIO.BOTH, callback=handle_encoder2A)

try:
    while True:
        # Print the encoder positions, scaling them
        print("Encoder 1 (Left): {:.2f} | Encoder 2 (Right): {:.2f}".format(
            encoderPos1 * (210.48666 / (12 * 34 * 2.36)),
            # encoderPos2 * (210.48666 / (12 * 34 * 2.36))
        ))
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()
