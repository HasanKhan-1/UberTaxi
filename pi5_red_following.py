# import RPi.GPIO as GPIO
# import time

# in1 = 6
# in2 = 5
# in3 = 25
# in4 = 24

# ena_top = 26  # for forwards for speed, en1
# ena_bottom = 16 # for forwards for speed, en2
# enb_top = 23 # backwards for speed, en1b
# enb_bottom = 22 # backwards for speed, en2b

# # Set up GPIO mode
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

# # Set up GPIO pins
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)
# GPIO.setup(in3, GPIO.OUT)
# GPIO.setup(in4, GPIO.OUT)
# GPIO.setup(en1, GPIO.OUT)
# GPIO.setup(en2, GPIO.OUT)

# # Initialize PWM for speed control
# pwm1 = GPIO.PWM(ena_top, 100)  # 100 Hz frequency
# pwm2 = GPIO.PWM(ena_bottom, 100)  # 100 Hz frequency

# # Start PWM with 0% duty cycle (motor stopped)
# pwm1.start(0)
# pwm2.start(0)

# def stop_motors():
#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in2, GPIO.LOW)
#     GPIO.output(in3, GPIO.LOW)
#     GPIO.output(in4, GPIO.LOW)
#     pwm1.ChangeDutyCycle(0)
#     pwm2.ChangeDutyCycle(0)

# def move_forward(speed):
#     GPIO.output(in1, GPIO.HIGH)
#     GPIO.output(in2, GPIO.LOW)
#     GPIO.output(in3, GPIO.HIGH)
#     GPIO.output(in4, GPIO.LOW)
#     pwm1.ChangeDutyCycle(speed)
#     pwm2.ChangeDutyCycle(speed)

# def move_spin(speed):
#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in2, GPIO.HIGH)
#     GPIO.output(in3, GPIO.HIGH)
#     GPIO.output(in4, GPIO.LOW)
#     pwm1.ChangeDutyCycle(speed)
#     pwm2.ChangeDutyCycle(speed)

# def move_backwards(speed):
#     GPIO.output(in1, GPIO.LOW)
#     GPIO.output(in2, GPIO.HIGH)
#     GPIO.output(in3, GPIO.LOW)
#     GPIO.output(in4, GPIO.HIGH)
#     pwm1.ChangeDutyCycle(speed)
#     pwm2.ChangeDutyCycle(speed)

# if __name__ == "__main__":
#     try:
#         stop_motors()
#         while True:
#             ret, frame = cap.read()
#             low_b = np.uint8([0, 0, 153 ]) # red low threshold
#             high_b = np.uint8([102, 102, 255]) # red high threshold
#             mask = cv2.inRange(frame, low_b, high_b )
#             contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
            
#             if len(contours) > 0 :
#                 c = max(contours, key=cv2.contourArea)
#                 M = cv2.moments(c)
#                 if M["m00"] !=0 :
#                     cx = int(M['m10']/M['m00'])
#                     cy = int(M['m01']/M['m00'])
#                     print("CX : "+str(cx)+"  CY : "+str(cy))

#                     if cx >= 160 :
#                         print("Turn Left")
                        
#                     if cx <120 and cx > 40 :
#                         print("Straight, on track")
#                         move_forward(100)  # Move forward with 100% speed
#                         time.sleep(5)  # Move forward for 5 seconds
#                         stop_motors()
#                         time.sleep(2)  # Stop for 2 seconds
#             else :
#                 print("I don't see the line")
#                 GPIO.output(in1, GPIO.LOW)
#                 GPIO.output(in2, GPIO.LOW)

#                 GPIO.output(in3, GPIO.LOW)
#                 GPIO.output(in4, GPIO.LOW)

#             cv2.imshow("Mask",mask)
#             cv2.imshow("Frame",frame)
#             cv2.waitKey(1)

#     except KeyboardInterrupt:
#         pass
#     finally:
#         stop_motors()
#         GPIO.cleanup()

from gpiozero import OutputDevice, PWMOutputDevice
import cv2
import numpy as np
import time

# Motor control pins
in1 = 6
in2 = 5
in3 = 25
in4 = 24

# PWM speed control pins
ena_top = 26   # Forward speed control
ena_bottom = 16  # Forward speed control
enb_top = 23  # Backward speed control
enb_bottom = 22  # Backward speed control

# Initialize motor control pins
motor_in1 = OutputDevice(in1)
motor_in2 = OutputDevice(in2)
motor_in3 = OutputDevice(in3)
motor_in4 = OutputDevice(in4)

# Initialize PWM for speed control
pwm_ena_top = PWMOutputDevice(ena_top, initial_value=0)
pwm_ena_bottom = PWMOutputDevice(ena_bottom, initial_value=0)
pwm_enb_top = PWMOutputDevice(enb_top, initial_value=0)
pwm_enb_bottom = PWMOutputDevice(enb_bottom, initial_value=0)

def stop_motors():
    motor_in1.off()
    motor_in2.off()
    motor_in3.off()
    motor_in4.off()
    pwm_ena_top.value = 0
    pwm_ena_bottom.value = 0
    pwm_enb_top.value = 0
    pwm_enb_bottom.value = 0

def move_forward(speed):
    motor_in1.on()
    motor_in2.off()
    motor_in3.on()
    motor_in4.off()
    pwm_ena_top.value = speed / 100
    pwm_ena_bottom.value = speed / 100

def move_spin(speed):
    motor_in1.off()
    motor_in2.on()
    motor_in3.on()
    motor_in4.off()
    pwm_ena_top.value = speed / 100
    pwm_ena_bottom.value = speed / 100

def move_backwards(speed):
    motor_in1.off()
    motor_in2.on()
    motor_in3.off()
    motor_in4.on()
    pwm_enb_top.value = speed / 100
    pwm_enb_bottom.value = speed / 100

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

                    if cx >= 160:
                        print("Turn Left")
                        move_spin(50)  # Adjust speed as needed
                        time.sleep(0.5)
                        stop_motors()
                    
                    elif 40 < cx < 120:
                        print("Straight, on track")
                        move_forward(80)  # Adjust speed to 80%
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
