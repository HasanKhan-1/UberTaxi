import cv2 as cv
import numpy as np
import smbus2
import time 

I2C_BUS = 1 
ELEGOO_ADDRESS = 0X8 # change to match Elegoo's I2C address 

bus = smbus2.SMBus(I2C_BUS)

def send_motor_command(command): 
    try: 
        bus.write_byte(ELEGOO_ADDRESS, command)
        print(f"sent command")
    except Exception as e: 
            print(f"i2c error")


def detect_red_line():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # [*1] Set resolution
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels

    # [*2] Set frame rate
    cap.set(cv.CAP_PROP_FPS, 30)  # Set to 30 frames per second

#     # [*3] Define HSV range for red color
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_lower_2 = np.array([160, 100, 100])
    red_upper_2 = np.array([180, 255, 255])

    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

#         # Resize frame for consistency
        frame = cv.resize(frame, (480, 480))

#         # Convert to HSV color space
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

#         # Create masks for red color
        mask1 = cv.inRange(hsv, red_lower, red_upper)
        mask2 = cv.inRange(hsv, red_lower_2, red_upper_2)
        mask = cv.bitwise_or(mask1, mask2)

#         # Apply mask to isolate red regions
        red_regions = cv.bitwise_and(frame, frame, mask=mask)

#         # Convert the mask to grayscale for edge detection
        gray = cv.cvtColor(red_regions, cv.COLOR_BGR2GRAY)

#         # [*4] Apply Canny edge detection
        edges = cv.Canny(gray, 50, 150)

#         # [*5] Use HoughLinesP to detect line segments
        lines = cv.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

        # Draw the detected lines on the original frame
        if lines is not None:
            print("Red line detected, moving wheels")
            send_motor_command(1)
            for line in lines:
                x1, y1, x2, y2 = line[0]  # Unpack line endpoints
                cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw line in green
        else:
            print("No red line detected")
            send_motor_command(0)
            
        # Display the original frame with detected lines
        cv.imshow('Red Line Detection', frame)

        # Break loop on user interrupt (e.g., 'q' key press)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

# Run the function
detect_red_line()

# import cv2 as cv
# import numpy as np
# import smbus2

# I2C_BUS = 1
# ELEGOO_ADDRESS = 0x8  # Change to match Elegoo's I2C address
# bus = smbus2.SMBus(I2C_BUS)

# def send_motor_command(command): 
#     try: 
#         bus.write_byte(ELEGOO_ADDRESS, command)
#         print(f"Sent command: {command}")
#     except Exception as e: 
#         print(f"I2C error: {e}")

# def detect_red_line():
#     cap = cv.VideoCapture(0)

#     cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

#     # Define HSV range for **bright red**
#     red_lower = np.array([0, 150, 180])
#     red_upper = np.array([10, 255, 255])
#     red_lower_2 = np.array([170, 150, 180])
#     red_upper_2 = np.array([180, 255, 255])

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to capture frame")
#             break

#         frame = cv.resize(frame, (480, 480))
#         hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

#         # Mask for bright red
#         mask1 = cv.inRange(hsv, red_lower, red_upper)
#         mask2 = cv.inRange(hsv, red_lower_2, red_upper_2)
#         mask = cv.bitwise_or(mask1, mask2)

#         # Find red contours
#         contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#         if contours:
#             largest_contour = max(contours, key=cv.contourArea)
#             M = cv.moments(largest_contour)
#             if M["m00"] != 0:
#                 cx = int(M["m10"] / M["m00"])  # X coordinate of centroid
#                 cy = int(M["m01"] / M["m00"])  # Y coordinate (not used for decisions)

#                 # Define three sections of the frame
#                 left_bound = frame.shape[1] // 3
#                 right_bound = 2 * (frame.shape[1] // 3)

#                 if cx < left_bound:
#                     print("Turn LEFT")
#                     send_motor_command(2)  # Command for left turn
#                 elif cx > right_bound:
#                     print("Turn RIGHT")
#                     send_motor_command(3)  # Command for right turn
#                 else:
#                     print("Go STRAIGHT")
#                     send_motor_command(1)  # Move forward
#             else:
#                 print("Centroid calculation error")
#                 send_motor_command(0)  # Stop if there's an issue
#         else:
#             print("No red line detected")
#             send_motor_command(0)  # Stop if no red is detected

#         # Draw detected contour and centroid
#         cv.drawContours(frame, contours, -1, (0, 255, 0), 2)
#         if 'cx' in locals():
#             cv.circle(frame, (cx, cy), 5, (255, 0, 0), -1)  # Draw centroid

#         cv.imshow('Red Line Detection', frame)

#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv.destroyAllWindows()

# detect_red_line()