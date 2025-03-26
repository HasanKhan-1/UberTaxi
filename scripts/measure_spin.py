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

TARGET_STEPS = 1000

# Conversion factor
CONVERSION_FACTOR = 210.48666 / (12 * 34 * 2.36)

def print_encoder_values():
    """Print the current values of both encoders with conversion."""
    left_converted = encoder1.steps * CONVERSION_FACTOR
    right_converted = encoder2.steps * CONVERSION_FACTOR
    print(f"Left: ({left_converted:.2f}) | Right: ({right_converted:.2f})")

def move_spin(speed):
    """Spin the robot in place at specified speed (0-1)."""
    print(f"\nStarting spin at {speed*100}% power")
    # Left motor forward
    IN1.off()
    IN2.on()
    # Right motor backward
    IN3.off()
    IN4.on()
    
    # Set PWM speeds (very low value for slow spin)
    ENA.value = speed
    ENAb.value = speed
    ENB.value = speed
    ENBb.value = speed

def stop_motors():
    """Stop all motors"""
    print("\nStopping motors")
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    ENA.value = 0
    ENB.value = 0
    ENAb.value = 0
    ENBb.value = 0

try:
    # Start very slow spin (adjust this value as needed)
    move_spin(0.15)  
    
    if abs(encoder1.steps) >= TARGET_STEPS and abs(encoder2.steps) >= TARGET_STEPS:
    stop_motors()
    print("Target reached")
    exit()  # Stops the script

    while True:
        print_encoder_values()
        sleep(0.1)  # Update rate for encoder readings

except KeyboardInterrupt:
    print("\nUser interrupted script")

finally:
    stop_motors()
    # Cleanup resources
    encoder1.close()
    encoder2.close()
    IN1.close()
    IN2.close()
    IN3.close()
    IN4.close()
    ENA.close()
    ENB.close()
    ENAb.close()
    ENBb.close()
