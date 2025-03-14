import cv2 as cv
import numpy as np

def detect_red_line():
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Manual exposure
    cap.set(cv.CAP_PROP_EXPOSURE, -4)

    cv.namedWindow('Controls')
    cv.createTrackbar('Hue Min', 'Controls', 0, 179, lambda x: None)
    cv.createTrackbar('Hue Max', 'Controls', 10, 179, lambda x: None)
    cv.createTrackbar('Sat Min', 'Controls', 100, 255, lambda x: None)
    cv.createTrackbar('Val Min', 'Controls', 100, 255, lambda x: None)

    prev_error = 0
    integral = 0
    debug_text = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        frame = cv.resize(frame, (480, 480))
        blurred = cv.GaussianBlur(frame, (5,5), 0)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
        hsv[:,:,2] = cv.equalizeHist(hsv[:,:,2])

        # Get current trackbar values
        h_min = cv.getTrackbarPos('Hue Min', 'Controls')
        h_max = cv.getTrackbarPos('Hue Max', 'Controls')
        s_min = cv.getTrackbarPos('Sat Min', 'Controls')
        v_min = cv.getTrackbarPos('Val Min', 'Controls')

        # Define HSV ranges
        red_lower = np.array([h_min, s_min, v_min])
        red_upper = np.array([h_max, 255, 255])
        red_lower_2 = np.array([170, s_min, v_min])
        red_upper_2 = np.array([179, 255, 255])

        # Create mask
        mask1 = cv.inRange(hsv, red_lower, red_upper)
        mask2 = cv.inRange(hsv, red_lower_2, red_upper_2)
        mask = cv.bitwise_or(mask1, mask2)

        # Noise reduction
        kernel = np.ones((5,5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        min_contour_area = 500
        valid_contours = [c for c in contours if cv.contourArea(c) > min_contour_area]

        if valid_contours:
            largest_contour = max(valid_contours, key=cv.contourArea)
            M = cv.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                frame_center = frame.shape[1] // 2
                error = cx - frame_center

                # PID control
                KP, KI, KD = 0.5, 0.01, 0.1
                integral += error
                derivative = error - prev_error
                output = KP*error + KI*integral + KD*derivative
                prev_error = error

                # Decision making with debug info
                turn_intensity = int(abs(output))
                if output < -20:
                    action = f"TURN LEFT (Intensity: {turn_intensity})"
                elif output > 20:
                    action = f"TURN RIGHT (Intensity: {turn_intensity})"
                else:
                    action = f"GO STRAIGHT (Confidence: {turn_intensity})"
                
                debug_text = f"Line detected | {action} | Centroid X: {cx} | Error: {error:.1f}"
            else:
                debug_text = "Centroid calculation error"
        else:
            debug_text = "No line detected - STOPPING"

        # Display debug info
        print(debug_text)
        cv.putText(frame, debug_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Visual feedback
        if valid_contours:
            cv.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
            cv.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
            cv.line(frame, (frame_center, 0), (frame_center, frame.shape[0]), (0, 0, 255), 2)

        cv.imshow('Red Line Detection', frame)
        cv.imshow('Mask', mask)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

detect_red_line()
