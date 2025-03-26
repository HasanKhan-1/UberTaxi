import cv2
import numpy as np
import time
from motors import MotorController
from pid_controller import PID

class VisionProcessor:
    def __init__(self, motor_controller, pid_controller, setpoint=80):
        """Initialize the vision processor with motor and PID controllers."""
        self.motor_controller = motor_controller
        self.pid = pid_controller
        self.setpoint = setpoint
        self.cap = cv2.VideoCapture(0)  # Initialize camera
        self.cap.set(3, 160)  # Set frame width
        self.cap.set(4, 120)  # Set frame height

    def process_frame(self):
        """Process the camera frame to detect the red line."""
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        # Define red color thresholds
        low_b = np.array([0, 0, 153], dtype=np.uint8)  # Red low threshold
        high_b = np.array([102, 102, 255], dtype=np.uint8)  # Red high threshold
        mask = cv2.inRange(frame, low_b, high_b)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours, frame, mask

    def follow_line(self):
        """Main loop to follow the red line."""
        try:
            self.motor_controller.stop_motors()
            while True:
                contours, frame, mask = self.process_frame()
                if contours is None:
                    continue

                if contours:
                    c = max(contours, key=cv2.contourArea)
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        print(f"CX: {cx}, CY: {cy}")

                        # Calculate PID output
                        pid_output = self.pid.compute(self.setpoint, cx)
                        speed = 0.5 + pid_output  # Adjust base speed with PID output
                        speed = max(0, min(1, speed))  # Ensure speed is within [0, 1]

                        if cx >= 160:
                            print("Turn Left")
                            self.motor_controller.move_spin(speed)
                            time.sleep(0.5)
                            self.motor_controller.stop_motors()
                        elif 40 < cx < 120:
                            print("Straight, on track")
                            self.motor_controller.move_forward(speed)
                            time.sleep(2)
                            self.motor_controller.stop_motors()
                            time.sleep(1)
                    else:
                        self.motor_controller.stop_motors()
                else:
                    print("I don't see the line")
                    self.motor_controller.stop_motors()

                cv2.imshow("Mask", mask)
                cv2.imshow("Frame", frame)
                cv2.waitKey(1)

        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()

    def cleanup(self):
        """Release resources."""
        self.motor_controller.stop_motors()
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Initialize motor controller
    motor_controller = MotorController()

    # Initialize PID controller
    pid = PID(Kp=0.1, Ki=0.01, Kd=0.05)

    # Initialize vision processor
    vision_processor = VisionProcessor(motor_controller, pid, setpoint=80)

    # Start following the line
    vision_processor.follow_line()