# from gpiozero import PWMOutputDevice, DigitalOutputDevice
# from time import sleep

# # Motor Pins
# IN1 = DigitalOutputDevice(6)
# IN2 = DigitalOutputDevice(5)
# IN3 = DigitalOutputDevice(25)
# IN4 = DigitalOutputDevice(24)
# ENA = PWMOutputDevice(17)  # Speed control (PWM)
# ENB = PWMOutputDevice(22)  # Speed control (PWM)

# ENAb = PWMOutputDevice(27)  # Speed control (PWM)
# ENBb = PWMOutputDevice(23)  # Speed control (PWM)

# # Setup PWM for speed control
# ENA.value = 0.5  # 50% speed
# ENB.value = 0.5
# ENAb.value = 0.5  # 50% speed
# ENBb.value = 0.5


# def move_forward():
#     """Move both motors forward."""
#     print("Moving forward")
#     IN1.on()
#     IN2.off()
#     IN3.on()
#     IN4.off()
#     ENA.value = 0.5
#     ENB.value = 0.5
#     ENAb.value = 0.5
#     ENBb.value = 0.5

# def move_backward():
#     """Move both motors backward."""
#     print("Moving backward")
#     IN1.off()
#     IN2.on()
#     IN3.off()
#     IN4.on()
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
#         sleep(2)  # Move forward for 2 seconds
#         stop_motors()
#         sleep(1)  # Stop for 1 second
#         move_backward()
#         sleep(2)  # Move backward for 2 seconds
#         stop_motors()
#     # except KeyboardInterrupt:
#     #     pass
#     # finally:
#     #     stop_motors()


from gpiozero import LED
from time import sleep

# List of all usable GPIO pins (excluding power, ground, and reserved pins)
gpio_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 
             16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Create LED objects for each pin
leds = [LED(pin) for pin in gpio_pins]

# Turn ON all GPIO pins
for led in leds:
    led.on()

print("All GPIO pins are ON!")

# Keep running to maintain the state
try:
    while True:
        sleep(1)  # Keep the program running
except KeyboardInterrupt:
    print("Turning off all GPIO pins...")
    for led in leds:
        led.off()
