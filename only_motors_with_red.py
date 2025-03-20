import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)


in1 = 6
in2 = 5
in3 = 22
in4 = 27

en1 = 16 # for forwards for speed
en2 = 17 # for forwards for speed
en1b = 26 # backwards for speed
en2b = 23 # backwards for speed
# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)

# Initialize PWM for speed control
pwm1 = GPIO.PWM(en1, 100)  # 100 Hz frequency
pwm2 = GPIO.PWM(en2, 100)  # 100 Hz frequency

# Start PWM with 0% duty cycle (motor stopped)
pwm1.start(0)
pwm2.start(0)

def stop_motors():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

def move_forward(speed):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)

def move_left(speedright, speedleft):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(speedright)
    pwm2.ChangeDutyCycle(speedleft)

def move_right(speedright, speedleft):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(speedright)
    pwm2.ChangeDutyCycle(speedleft)


if __name__ == "__main__":
    try:
        stop_motors()
        while True:
            ret, frame = cap.read()
            low_b = np.uint8([0, 0, 153 ]) # red low threshold
            high_b = np.uint8([102, 102, 255]) # red high threshold
            mask = cv2.inRange(frame, low_b, high_b )
            contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
            
            if len(contours) > 0 :
                c = max(contours, key=cv2.contourArea)
                M = cv2.moments(c)
                if M["m00"] !=0 :
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    print("CX : "+str(cx)+"  CY : "+str(cy))

                    if cx >= 160 :
                        print("Turn Left")
                        move_left(20, 10)
                        
                    if cx <120 and cx > 40 :
                        print("Straight, on track")
                        move_forward(20)  # Move forward with 100% speed
                        time.sleep(5)  # Move forward for 5 seconds
                        stop_motors()
                        time.sleep(2)  # Stop for 2 seconds
            else :
                print("I don't see the line")
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)

                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.LOW)

            cv2.imshow("Mask",mask)
            cv2.imshow("Frame",frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        GPIO.cleanup()