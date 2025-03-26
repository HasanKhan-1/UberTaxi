# from picamera2 import Picamera2
# import cv2


# # Initialize the camera
# picam2 = Picamera2()
# picam2.preview_configuration.main.size = (640, 480)  # Set resolution
# picam2.preview_configuration.main.format = "RGB888"
# picam2.configure("preview")

# # Start the camera
# picam2.start()

# while True:
#     frame = picam2.capture_array()  # Capture frame
#     cv2.imshow("PiCamera Stream", frame)  # Display the stream
    
#     # Break on 'q' key press
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# Cleanup
# cv2.destroyAllWindows()
# picam2.close()

import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize PiCamera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Set resolution
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

while True:
    frame = picam2.capture_array()  # Capture frame

    # Create a mask where green is dominant
    green_mask = (frame[:, :, 1] > frame[:, :, 0]) & (frame[:, :, 1] > frame[:, :, 2])
    
    # Convert boolean mask to uint8 (0s and 255s)
    mask = green_mask.astype(np.uint8) * 255

    # Apply the mask to highlight green areas
    green_highlighted = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the original frame and the detected green areas
    cv2.imshow("Original Stream", frame)
    cv2.imshow("Green Detection", green_highlighted)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.close()