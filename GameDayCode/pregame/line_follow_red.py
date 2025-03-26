from gpiozero import RotaryEncoder, PWMOutputDevice, DigitalOutputDevice, AngularServo
from time import sleep
import cv2
import numpy as np
import time
from simple_pid import PID  

# Motor Pins
IN1 = DigitalOutputDevice(14)
IN2 = DigitalOutputDevice(5)
IN3 = DigitalOutputDevice(2)
IN4 = DigitalOutputDevice(3)
ENA = PWMOutputDevice(4)  # Speed control (PWM)

ENB = PWMOutputDevice(23)  # Speed control (PWM)

ENAb = PWMOutputDevice(27)  # Speed control (PWM)
ENBb = PWMOutputDevice(24)  # Speed control (PWM)

# Initialize PID controller
pid = PID(0.1, 0.05, 0.05)  
pid.output_limits = (-0.1, 0.1)  # Ensure PID doesn't overcorrect

# Encoders + Encoder Definitions 

encoder1 = RotaryEncoder(a=20, b=21, max_steps=0)  
encoder2 = RotaryEncoder(a=10, b=9, max_steps=0)  

TARGET_STEPS = 600
# Conversion factor
CONVERSION_FACTOR = 210.48666 / (12 * 34 * 2.36)


def move_forward(base_speed, correction):
    """Move both motors forward with PID correction applied."""
    print(f"Moving forward")
    IN1.off()
    IN2.on()
    IN3.on()
    IN4.off()
    
    left_speed = base_speed*0.7
    right_speed = base_speed

    # left motor    
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))

    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))

def move_left(base_speed, correction):
    """Move robot left by slowing down left motor and speeding up right motor."""
    print(f"Moving left, Correction: {correction}")
    IN1.off()
    IN2.on()
    IN3.on()
    IN4.off()

    # Slow down left motor, speed up right motor
    left_speed = base_speed*0.9 - 0.05  # Decrease left motor speed (adjust as needed)
    right_speed = base_speed + 0.08  # Increase right motor speed (adjust as needed)

    # Apply the speeds to the motors
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))
    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))


def move_right(base_speed, correction):
    """Move robot left by slowing down left motor and speeding up right motor."""
    print(f"Moving left, Correction: {correction}")
    IN1.off()
    IN2.on()
    IN3.on()
    IN4.off()
    
    # Slow down left motor, speed up right motor
    left_speed = base_speed*0.8 + 0.13  # Increase left motor speed (adjust as needed)
    right_speed = base_speed - 0.13  # Decrease right motor speed (adjust as needed)

    # Apply the speeds to the motors
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))
    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))


def move_backwards(base_speed, correction):
    """Move both motors forward with PID correction applied."""
    print(f"Moving forward")
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    
    left_speed = base_speed - correction
    right_speed = base_speed + correction

    # left motor    
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))

    # right motor
    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))

def move_spin(speed):
    """Spin the robot in place."""
    print("Spinning")
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()

    ENA.value = max(0, min(1, speed))
    ENAb.value = max(0, min(1, speed))

    # right motor
    ENB.value = max(0, min(1, speed))
    ENBb.value = max(0, min(1, speed))

def stop_motors():
    """Stop both motors."""
    print("Stopping motors")
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    ENA.value = 0
    ENB.value = 0
    ENAb.value = 0
    ENBb.value = 0


if __name__ == "__main__":
    try:
        stop_motors()
        cap = cv2.VideoCapture(0)  # Initialize camera
        cap.set(3, 160)
        cap.set(4, 120)
        servo_moved = False  # Track if the servo has already moved

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            low_b = np.array([0, 0, 153], dtype=np.uint8)  # Red low threshold
            high_b = np.array([102, 102, 255], dtype=np.uint8)  # Red high threshold
            mask = cv2.inRange(frame, low_b, high_b)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            

            low_blue = np.array([102, 0, 0], dtype=np.uint8)  # Blue low threshold
            high_blue = np.array([255, 102, 102], dtype=np.uint8)  # Blue high threshold
            blue_mask = cv2.inRange(frame, low_blue, high_blue)
            blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cv2.imshow("Mask", mask)
            cv2.imshow("Blue Mask", blue_mask)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                cv2.drawContours(frame, [c], -1, (0, 255, 0), 1)

                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    print(f"CX: {cx}, CY: {cy}")

                    correction = pid(cx)  
                    if cx < 120 and cx > 50:
                        print("Straight, on track")
                        move_forward(0.2, correction)  # Move with PID correction
                        print(f"Correction: {correction}")
                    elif cx >= 120: 
                        print("Turn left")
                        move_left(0.15, correction)  # Move left by slowing down left motor and speeding up right motor
                    elif cx <=50 :
                        print("Turn Right")
                        move_right(0.15, correction)  # Move left by slowing down left motor and speeding up right motor

            elif len(blue_contours) > 0 and not servo_moved:  
                servo = AngularServo(19, min_angle=0, max_angle=180, min_pulse_width = 0.5/1000, max_pulse_width=2.5/1000) 
                servo_moved = False  

                print("Detected blue. Stopping.")
                stop_motors()
                sleep(3)
                
                print("Moving servo")
                servo.angle = 52
                sleep(1)
                
                print("Lego man is in garage")
                servo_moved = True  
                sleep(1)
                
                move_spin(0.15)
                left_converted = encoder1.steps * CONVERSION_FACTOR
                right_converted = encoder2.steps * CONVERSION_FACTOR
                 
                if abs(encoder1.steps) >= TARGET_STEPS and abs(encoder2.steps) >= TARGET_STEPS:
                    stop_motors()
                    print("Target reached")
                    sleep(1) 

                print("Spinning")
                move_forward(0.2, correction)
                sleep(1)

            else:
                stop_motors()
                print("I don't see the line")

    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        cap.release()
        cv2.destroyAllWindows()