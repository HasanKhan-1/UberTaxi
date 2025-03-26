from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep
import cv2 as cv
import numpy as np

# Motor Pins
IN1 = DigitalOutputDevice(17)
IN2 = DigitalOutputDevice(18)
IN3 = DigitalOutputDevice(22)
IN4 = DigitalOutputDevice(23)

ENAf = PWMOutputDevice(24)  # Speed control (PWM)
ENBf = PWMOutputDevice(25)  # Speed control (PWM)

ENAr = PWMOutputDevice(5)  # Speed control (PWM)
ENBr = PWMOutputDevice(6)  # Speed control (PWM)

# Camera Setup
cap = cv.VideoCapture(0)

# Motor Control Functions
def stop_motors():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    ENAf.value = 0
    ENAr.value = 0

    ENBf.value = 0
    ENBr.value = 0

def move_forward(speed=0.5):
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    ENAf.value = speed
    ENAr.value = speed
    ENBf.value = speed
    ENBr.value = speed

def turn_left(speed=0.5):
    slow = 0.25
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    ENAf.value = speed
    ENAr.value = speed
    ENBf.value = slow
    ENBr.value = slow


def turn_right(speed=0.5):
    slow = 0.25
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    ENAf.value = slow
    ENAr.value = slow
    ENBf.value = speed
    ENBr.value = speed


def process_frame(frame):
    # Convert to HSV for better color detection
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)
    
    # Find contours
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        M = cv.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            frame_center = frame.shape[1] // 2
            if cx < frame_center - 50:
                turn_left(0.6)
                # move_forward(0.5)
            elif cx > frame_center + 50:
                # move_forward(0.5)
                turn_right(0.6)
            else:
                move_forward(0.5)
        else:
            stop_motors()
    else:
        stop_motors()

def main():
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            process_frame(frame)
            cv.imshow('Frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()
