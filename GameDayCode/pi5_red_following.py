from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep
import cv2
import numpy as np
import time
from simple_pid import PID  # Import the PID controller

# Motor Pins
IN1 = DigitalOutputDevice(6)
IN2 = DigitalOutputDevice(5)
IN3 = DigitalOutputDevice(25)
IN4 = DigitalOutputDevice(24)
ENA = PWMOutputDevice(17)  # Speed control (PWM)
ENB = PWMOutputDevice(22)  # Speed control (PWM)

ENAb = PWMOutputDevice(27)  # Speed control (PWM)
ENBb = PWMOutputDevice(23)  # Speed control (PWM)

# Setup PWM for speed control
ENA.value = 0.5  # 50% speed
ENB.value = 0.5
ENAb.value = 0.5  # 50% speed
ENBb.value = 0.5

# Initialize PID controller
pid = PID(0.1, 0.01, 0.05, setpoint=80)  # Desired position (center of the frame)

def move_forward(speed):
    """Move both motors forward with a given speed."""
    print("Moving forward")
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    ENA.value = speed
    ENB.value = speed
    ENAb.value = speed
    ENBb.value = speed

def move_backward(speed):
    """Move both motors backward with a given speed."""
    print("Moving backward")
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    ENA.value = speed
    ENB.value = speed
    ENAb.value = speed
    ENBb.value = speed

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

def move_spin(speed):
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    ENA.value = speed
    ENB.value = speed
    ENAb.value = speed
    ENBb.value = speed

if __name__ == "__main__":
    try:
        stop_motors()
        cap = cv2.VideoCapture(0)  # Initialize camera
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            low_b = np.array([0, 0, 153], dtype=np.uint8)  # Red low threshold
            high_b = np.array([102, 102, 255], dtype=np.uint8)  # Red high threshold
            mask = cv2.inRange(frame, low_b, high_b)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    print(f"CX: {cx}, CY: {cy}")

                    # Calculate PID output
                    pid_output = pid(cx)
                    speed = 0.5 + pid_output  # Adjust base speed with PID output
                    speed = max(0, min(1, speed))  # Ensure speed is within [0, 1]

                    if cx >= 160:
                        print("Turn Left")
                        move_spin(speed)  # Adjust speed as needed
                        time.sleep(0.5)
                        stop_motors()
                    
                    elif 40 < cx < 120:
                        print("Straight, on track")
                        move_forward(speed)  # Adjust speed to 80%
                        time.sleep(2)
                        stop_motors()
                        time.sleep(1)
                else:
                    stop_motors()
            else:
                print("I don't see the line")
                stop_motors()

            cv2.imshow("Mask", mask)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        cap.release()
        cv2.destroyAllWindows()