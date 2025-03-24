from gpiozero import DigitalOutputDevice
import time

# Define GPIO pins
data_pin = DigitalOutputDevice(16)   # Serial Data (DS)
latch_pin = DigitalOutputDevice(20)  # Latch Clock (ST_CP)
clock_pin = DigitalOutputDevice(21)  # Shift Clock (SH_CP)

def shift_out(bit_pattern):
    """Send an 8-bit pattern to the shift register."""
    latch_pin.off()  # Prepare to send data
    for bit in bit_pattern:
        data_pin.value = int(bit)  # Send each bit (1 or 0)
        clock_pin.on()  # Pulse clock to shift data
        clock_pin.off()
    latch_pin.on()  # Update outputs

# Example: Turn on LED connected to Q0 (First output of 74HC595)
ledpattern = "00000001"  # Binary pattern for turning ON the first LED
shift_out(ledpattern)
