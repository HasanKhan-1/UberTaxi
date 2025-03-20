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


if __name__ == "__main__":
    left_forward.on()
    left_backward.off()
    right_backward.on()
    right_forward.off()

