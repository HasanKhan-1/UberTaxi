import cv2
import numpy as np
from gpiozero import PWMOutputDevice, DigitalOutputDevice
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
# cx =0
# cy = 0
in1 = 0
# in2 used to be gpio 18
in2 = 2
in3 = 3
#in4 used to be gpio 23
in4 = 4

en1 = 5 # for forwards for speed
en2 = 25 # for forwards for speed
en1b = 6 # backwards for speed
en2b = 27 # backwards for speed

p1 = PWMOutputDevice(en1, frequency=100)
p2 = PWMOutputDevice(en1b, frequency=100)
p1.value = 1
p2.value = 1

p3 = PWMOutputDevice(en2, frequency=100)
p4 = PWMOutputDevice(en2b, frequency=100)
p3.value = 1
p4.value = 1

# left_forward = DigitalOutputDevice(in1)
# left_backward = DigitalOutputDevice(in2)

left_forward = DigitalOutputDevice(in1)
left_backward = DigitalOutputDevice(in2)
right_forward = DigitalOutputDevice(in3)
right_backward= DigitalOutputDevice(in4)


left_forward.off()
left_backward.off()
right_backward.off()
right_forward.off()

while True:
    ret, frame = cap.read()
    low_b = np.uint8([0, 0, 153 ])
    high_b = np.uint8([102, 102, 255])

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
                
                left_forward.off()
                left_backward.on() #2
                right_forward.off()
                right_backward.on() #4

                p4.value = 0.4 
                p2.value = 0.2 

                p1.value = 0.2
                p3.value = 0.2 

            if cx <120 and cx > 40 :
                print("Straight, on track")
                
                left_forward.on() 
                left_backward.off()

                right_forward.off()
                right_backward.on()

                p1.value = 0.25 # left forward speed
                p4.value = 0.20 # right
                p2.value = 0.25 # left             
                p3.value = 0.20 # right
                              

            if cx <=40 :
                print("Turn Right")
                left_forward.off()
                left_backward.on() #2
                right_forward.off()
                right_backward.on() #4

                p4.value = 0.2 # right backwards speed 
                p2.value = 0.4 # left backward speed

                p1.value = 0.4 # right forward speed
                p3.value = 0.4 # left forward speed

        cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
        cv2.drawContours(frame, c, -1, (0,255,0), 1)
    
    else :
        print("I don't see the line")
        left_forward.off()
        left_backward.off()
        right_backward.off()
        right_forward.off()

    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)

cap.release()
cv2.destroyAllWindows()

