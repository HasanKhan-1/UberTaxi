import cv2
import numpy as np
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Motor 
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
in1 = 17
# in2 used to be gpio 18
in2 = 27
in3 = 22
in4 = 23

en1 = 24 # for forwards for speed
en2 = 25 # for forwards for speed
en1b = 6 # backwards for speed
en2b = 5 # backwards for speed

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
    low_b = np.uint8([150,150,150])
    high_b = np.uint8([250, 250, 250])
    mask = cv2.inRange(frame, low_b, high_b )
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 120 :
                print("Turn Left")
                # in1_pin.on()
                # in2_pin.off()
                # in3_pin.off()
                # in4_pin.on()
                # speed = 0.5
                
                left_forward.off()
                left_backward.on()
                p1.value = 0.5
                p4.value = 0.5
                p2.value = 0.5
                
                right_backward.off()
                right_forward.on()
                p3.value = 0.5 
            
            if cx <120 and cx > 40 :
                print("Straight, on track")
                
                left_forward.off()
                left_backward.on()
                p1.value = 0.5
                p4.value = 0.5
                p2.value = 0.5
                
                right_backward.off()
                right_forward.on()
                p3.value = 0.5                 

            if cx <=40 :
                print("Turn Right")
                left_forward.off()
                left_backward.on() #2
                right_backward.on() #4
                right_forward.off()

                p4.value = 0.5 
                p2.value = 1

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
    if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
        left_forward.off()
        left_backward.off()
        right_backward.off()
        right_forward.off()
        break
cap.release()
cv2.destroyAllWindows()

