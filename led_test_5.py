from gpiozero import LED
from time import sleep

# LED Pin


led = LED(24)

def turn_on_led():
    """Turn on the LED."""
    print("Turning on LED")
    led.on()

def turn_off_led():
    """Turn off the LED."""
    print("Turning off LED")
    led.off()

if __name__ == "__main__":
    try:
        turn_on_led()
        sleep(2)  # Keep the LED on for 2 seconds
        turn_off_led()
    except KeyboardInterrupt:
        pass
    finally:
        turn_off_led()  # Make sure the LED is off  