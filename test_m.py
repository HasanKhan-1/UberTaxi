import cv2
import numpy as np
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)

in1 = 6
in2 = 5
in3 = 22
in4 = 27

en1 = 16 # for forwards for speed
en1b = 26 # backwards for speed

en2 = 17 # for forwards for speed
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

GPIO.setup(en1b, GPIO.OUT)
GPIO.setup(en2b, GPIO.OUT)
# Initialize PWM for speed control
p1 = GPIO.PWM(en1, 100)  # 100 Hz frequency
p1b = GPIO.PWM(en1b, 100)  # 100 Hz frequency

p2 = GPIO.PWM(en2, 100)  # 100 Hz frequency
p2b = GPIO.PWM(en2b, 100)  # 100 Hz frequency

# Start PWM with 0% duty cycle (motor stopped)
p1.start(0)
p2.start(0)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

GPIO.output(en1, GPIO.LOW)
GPIO.output(en1b, GPIO.LOW)

GPIO.output(en2, GPIO.LOW)
GPIO.output(en2b, GPIO.LOW)

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

                # left_forward.off()
                # left_backward.on() #2
                # right_forward.off()
                # right_backward.on() #4

                # p4.value = 0.4 
                # p2.value = 0.2 

                # p1.value = 0.2
                # p3.value = 0.2 

            if cx <120 and cx > 40 :
                print("Straight, on track")
                
                # forward
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)

                GPIO.output(in3, GPIO.LOW)
                GPIO.output(in4, GPIO.HIGH)

                # left_forward.on() 
                # left_backward.off()

                # right_forward.off()
                # right_backward.on()

                p1.ChangeDutyCycle(30) # left forward speed
                # p1b.value = 0.25 # right
                p2.ChangeDutyCycle(30) # left             
                # p2b.value = 0.20 # right

                p1b.ChangeDutyCycle(30) # left             
                p2b.ChangeDutyCycle(30) # left             

            if cx <=40 :
                print("Turn Right")
                # left_forward.off()
                # left_backward.on() #2
                # right_forward.off()
                # right_backward.on() #4

                # p4.value = 0.2 # right backwards speed 
                # p2.value = 0.4 # left backward speed

                # p1.value = 0.4 # right forward speed
                # p3.value = 0.4 # left forward speed

        cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
        cv2.drawContours(frame, c, -1, (0,255,0), 1)
    
    else :
        print("I don't see the line")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)

        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)

cap.release()
cv2.destroyAllWindows()

