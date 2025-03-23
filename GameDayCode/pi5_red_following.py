from gpiozero import PWMOutputDevice, DigitalOutputDevice, Servo, AngularServo
from time import sleep
import cv2
import numpy as np
import time
from simple_pid import PID  

# Motor Pins
IN1 = DigitalOutputDevice(6)
IN2 = DigitalOutputDevice(5)
IN3 = DigitalOutputDevice(25)
IN4 = DigitalOutputDevice(24)
ENA = PWMOutputDevice(17)  # Speed control (PWM)
ENB = PWMOutputDevice(22)  # Speed control (PWM)

ENAb = PWMOutputDevice(27)  # Speed control (PWM)
ENBb = PWMOutputDevice(23)  # Speed control (PWM)

# Initialize PID controller
pid = PID(0.1, 0.01, 0.05, setpoint=80)  # Setpoint is center of frame (adjust if needed)
pid.output_limits = (-0.1, 0.1)  # Ensure PID doesn't overcorrect

def move_forward(base_speed, correction):
    """Move both motors forward with PID correction applied."""
    print(f"Moving forward, Correction: {correction}")
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    
    left_speed = base_speed - correction
    right_speed = base_speed + correction

    # left motor    
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))

    # right motor
    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))

def move_left(base_speed, correction):
    """Move robot left by slowing down left motor and speeding up right motor."""
    print(f"Moving left, Correction: {correction}")
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()

    # Slow down left motor, speed up right motor
    left_speed = base_speed - 0.2  # Decrease left motor speed (adjust as needed)
    right_speed = base_speed + 0.2  # Increase right motor speed (adjust as needed)

    # Apply the speeds to the motors
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))
    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))


def move_right(base_speed, correction):
    """Move robot left by slowing down left motor and speeding up right motor."""
    print(f"Moving left, Correction: {correction}")
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()

    # Slow down left motor, speed up right motor
    left_speed = base_speed + 0.2  # Increase left motor speed (adjust as needed)
    right_speed = base_speed - 0.2  # Decrease right motor speed (adjust as needed)

    # Apply the speeds to the motors
    ENA.value = max(0, min(1, left_speed))
    ENAb.value = max(0, min(1, left_speed))
    ENB.value = max(0, min(1, right_speed))
    ENBb.value = max(0, min(1, right_speed))


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
                    # move_forward(0.5, correction)  # Move with PID correction
                    if cx < 120 and cx > 40:
                        print("Straight, on track")
                        move_forward(0.5, correction)  # Move with PID correction
                        time.sleep(0.1)  # Small delay for stability
                    elif cx >= 160: 
                        move_left(0.5, correction)  # Move left by slowing down left motor and speeding up right motor
                
                    elif cx <=40 :
                        print("Turn Right")
                        move_right(0.5, correction)  # Move left by slowing down left motor and speeding up right motor

            elif len(blue_contours) > 0:
                servo = AngularServo(16, min_angle=0, max_angle=180)


                print("Detected blue.Stopping.")
                stop_motors()
                print("moving servo")
                servo.angle = 30
                sleep(1)
                print("Lego man is in garage")

            else:
                    print("I don't see the line")

    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        cap.release()
        cv2.destroyAllWindows()
