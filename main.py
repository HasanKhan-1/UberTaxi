import cv2 as cv
import numpy as np
from smbus2 import SMBus, i2c_msg

def detect_red_line():
    
    bus = SMBus(1)
    elegoo_addy = 
    
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    
    # HSV threshold trackbars
    cv.namedWindow('Controls')
    cv.createTrackbar('Hue Min', 'Controls', 0, 179, lambda x: None)
    cv.createTrackbar('Hue Max', 'Controls', 10, 179, lambda x: None)
    cv.createTrackbar('Sat Min', 'Controls', 100, 255, lambda x: None)
    cv.createTrackbar('Val Min', 'Controls', 100, 255, lambda x: None)
    cv.createTrackbar('Area Threshold', 'Controls', 500, 5000, lambda x: None)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and convert to HSV
        frame = cv.resize(frame, (480, 480))
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Get HSV values from trackbars
        h_min = cv.getTrackbarPos('Hue Min', 'Controls')
        h_max = cv.getTrackbarPos('Hue Max', 'Controls')
        s_min = cv.getTrackbarPos('Sat Min', 'Controls')
        v_min = cv.getTrackbarPos('Val Min', 'Controls')
        area_thresh = cv.getTrackbarPos('Area Threshold', 'Controls')

        # Create red mask
        lower_red1 = np.array([h_min, s_min, v_min])
        upper_red1 = np.array([h_max, 255, 255])
        lower_red2 = np.array([170, s_min, v_min])
        upper_red2 = np.array([179, 255, 255])
        
        mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        mask = cv.bitwise_or(mask1, mask2)

        # Clean up mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Split frame into left/right halves
        center_x = frame.shape[1] // 2
        left_count = 0
        right_count = 0

        # Analyze contours
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > area_thresh:
                x, y, w, h = cv.boundingRect(cnt)  # Get bounding box of contour
                
                if x + w // 2 < center_x:  # Contour is on the left side
                    left_count += 1
                    cv.drawContours(frame, [cnt], -1, (0,255,0), 2)  # Green for left side
                else:  # Contour is on the right side
                    right_count += 1
                    cv.drawContours(frame, [cnt], -1, (255,0,0), 2)  # Blue for right side

        # Decision making based on counts
        action = "STOP"
        if left_count > right_count:
            action = "TURN LEFT"
        elif right_count > left_count:
            action = "TURN RIGHT"
        elif left_count == right_count and left_count > 0:
            action = "GO STRAIGHT"

        # Visual display
        cv.line(frame, (center_x, 0), (center_x, frame.shape[0]), (0,0,255), 2)  # Red line in the middle
        cv.putText(frame, f"Left: {left_count} | Right: {right_count}", (10, 30), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv.putText(frame, f"Action: {action}", (10, 60), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # Show frames
        cv.imshow('Red Line Detection', frame)
        cv.imshow('Mask', mask)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

detect_red_line()


