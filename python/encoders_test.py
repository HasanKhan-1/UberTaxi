from gpiozero import Button
from time import sleep

# Encoder 1 (Left) GPIO Pins
encoder1PinA = 17  # GPIO17
encoder1PinB = 22  # GPIO22

# Encoder 2 (Right) GPIO Pins
encoder2PinA = 7   # GPIO7
encoder2PinB = 1   # GPIO1

# Initialize encoder positions
encoderPos1 = 0
encoderPos2 = 0

# Define callback functions for encoders
def handle_encoder1A():
    global encoderPos1
    if encoder1A.is_pressed == encoder1B.is_pressed:
        encoderPos1 += 1
    else:
        encoderPos1 -= 1

def handle_encoder2A():
    global encoderPos2
    if encoder2A.is_pressed == encoder2B.is_pressed:
        encoderPos2 += 1
    else:
        encoderPos2 -= 1

# Setup gpiozero Buttons with pull-ups and debouncing
encoder1A = Button(encoder1PinA, pull_up=True, bounce_time=0.001)
encoder1B = Button(encoder1PinB, pull_up=True, bounce_time=0.001)

encoder2A = Button(encoder2PinA, pull_up=True, bounce_time=0.001)
encoder2B = Button(encoder2PinB, pull_up=True, bounce_time=0.001)

# Attach the event handlers
encoder1A.when_pressed = handle_encoder1A
encoder1A.when_released = handle_encoder1A

encoder2A.when_pressed = handle_encoder2A
encoder2A.when_released = handle_encoder2A

# Main loop to print encoder values
try:
    while True:
        print("Encoder 1 (Left): {:.2f} | Encoder 2 (Right): {:.2f}".format(
            encoderPos1 * (210.48666 / (12 * 34 * 2.36)),
            encoderPos2 * (210.48666 / (12 * 34 * 2.36))
        ))
        sleep(0.1)

except KeyboardInterrupt:
    print("Program interrupted")
