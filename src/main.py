from motors import MotorController
from vision import VisionProcessor
from serveo_movement import ServoController
from simple_pid import PID  # Assuming you have a PID controller implementation
import time

class RobotController:
    def __init__(self):
        """Initialize all components of the robot."""
        # Initialize motor controller
        self.motor_controller = MotorController()

        # Initialize PID controller for vision processing
        self.pid = PID(Kp=0.1, Ki=0.01, Kd=0.05)

        # Initialize vision processor
        self.vision_processor = VisionProcessor(self.motor_controller, self.pid, setpoint=80)

        # Initialize servo controller
        self.servo_controller = ServoController(pin=16)

    def run(self):
        """Run the robot's main functionality."""
        try:
            print("Starting robot...")
            
            # Example: Move servo to an initial position
            self.servo_controller.move_to_position(0.3, delay=1)

            self.motor_controller.move_spin(0.5)
            # Start vision-based line following
            # self.vision_processor.follow_line()

        except KeyboardInterrupt:
            print("Robot stopped by user.")
        finally:
            # Stop motors and clean up resources
            self.motor_controller.stop_motors()
            self.vision_processor.cleanup()
            print("Robot shutdown complete.")

if __name__ == "__main__":
    robot = RobotController()
    robot.run()