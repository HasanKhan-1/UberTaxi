# from gpiozero import PWMOutputDevice, DigitalOutputDevice
# from time import sleep
# import cv2
# import numpy as np
# import time
# from simple_pid import PID  

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

# # Initialize PID controller
# pid = PID(0.1, 0.01, 0.05, setpoint=80)  

# def move_forward(speed):
#     """Move both motors forward with a given speed."""
#     print("Moving forward")
#     IN1.on()
#     IN2.off()
#     IN3.on()
#     IN4.off()
#     ENA.value = speed
#     ENB.value = speed
#     ENAb.value = speed
#     ENBb.value = speed

# def move_backward(speed):
#     """Move both motors backward with a given speed."""
#     print("Moving backward")
#     IN1.off()
#     IN2.on()
#     IN3.off()
#     IN4.on()
#     ENA.value = speed
#     ENB.value = speed
#     ENAb.value = speed
#     ENBb.value = speed

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

# def move_spin(speed):
#     IN1.off()
#     IN2.on()
#     IN3.off()
#     IN4.on()
#     ENA.value = speed
#     ENB.value = speed
#     ENAb.value = speed
#     ENBb.value = speed

# if __name__ == "__main__":
#     try:
#         stop_motors()
#         cap = cv2.VideoCapture(0)  # Initialize camera
        
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 continue
            
#             low_b = np.array([0, 0, 153], dtype=np.uint8)  # Red low threshold
#             high_b = np.array([102, 102, 255], dtype=np.uint8)  # Red high threshold
#             mask = cv2.inRange(frame, low_b, high_b)
#             contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
#             if contours:
#                 c = max(contours, key=cv2.contourArea)
#                 M = cv2.moments(c)
#                 cv2.drawContours(frame, c, -1, (0,255,0), 1)

#                 if M["m00"] != 0:
#                     cx = int(M['m10'] / M['m00'])
#                     cy = int(M['m01'] / M['m00'])
#                     print(f"CX: {cx}, CY: {cy}")

#                     error = cx - setpoint
#                     pid_output = pid(error) 

#                     if cx >= 160:
#                         print("Turn Left")
#                         # move_spin(speed)  # Adjust speed as needed
#                         # time.sleep(0.5)
#                         # stop_motors()
                    
#                     elif 40 < cx < 120:
#                         print("Straight, on track")
#                         move_forward(0.8)  
#                         time.sleep(2)
#                         stop_motors()
#                         time.sleep(1)
#                 else:
#                     stop_motors()
#             else:
#                 print("I don't see the line")
#                 stop_motors()

#             cv2.imshow("Mask", mask)
#             cv2.imshow("Frame", frame)
#             cv2.waitKey(1)

#     except KeyboardInterrupt:
#         pass
#     finally:
#         stop_motors()
#         cap.release()
#         cv2.destroyAllWindows()

from gpiozero import PWMOutputDevice, DigitalOutputDevice
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
            
            # Process Image
            low_b = np.array([0, 0, 153], dtype=np.uint8)  # Red low threshold
            high_b = np.array([102, 102, 255], dtype=np.uint8)  # Red high threshold
            mask = cv2.inRange(frame, low_b, high_b)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
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
                    # elif cx >= 160: 
                    #     move_left(0.5, correction)  # Move left by slowing down left motor and speeding up right motor
                
                else:
                    stop_motors()
            else:
                print("I don't see the line")
                stop_motors()

            # Show debug frames
            cv2.imshow("Mask", mask)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        cap.release()
        cv2.destroyAllWindows()
