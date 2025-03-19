import cv2
import numpy as np
from gpiozero import PWMOutputDevice, DigitalOutputDevice
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
in1 = 17
in2 = 18
in3 = 22
in4 = 23
en1 = 24 # for forwards 
en2 = 25 # for forwards 

p1 = PWMOutputDevice(en1, frequency=100)
p2 = PWMOutputDevice(en2, frequency=100)
in1_pin = DigitalOutputDevice(in1)
in2_pin = DigitalOutputDevice(in2)
in3_pin = DigitalOutputDevice(in3)
in4_pin = DigitalOutputDevice(in4)
p1.value = 0.5
p2.value = 0.5
in1_pin.off()
in2_pin.off()
in3_pin.off()
in4_pin.off()
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
                in1_pin.on()
                in2_pin.off()
                in3_pin.off()
                in4_pin.on()
            if cx <120 and cx > 40 :
                print("On Track!")
                in1_pin.on()
                in2_pin.off()
                in3_pin.on()
                in4_pin.off()
            if cx <=40 :
                print("Turn Right")
                in1_pin.off()
                in2_pin.on()
                in3_pin.on()
                in4_pin.off()
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
            cv2.drawContours(frame, c, -1, (0,255,0), 1)

    else :
        print("I don't see the line")
        in1_pin.off()
        in2_pin.off()
        in3_pin.off()
        in4_pin.off()
    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
        in1_pin.off()
        in2_pin.off()
        in3_pin.off()
        in4_pin.off()
        break
cap.release()
cv2.destroyAllWindows()

