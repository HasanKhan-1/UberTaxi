from gpiozero import Servo
from time import sleep

class ServoController:
    def __init__(self, pin=16, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000):
        self.servo = Servo(pin, min_pulse_width=min_pulse_width, max_pulse_width=max_pulse_width)

    def move_to_position(self, position, delay=1):
        self.servo.value = position
        print(f"Servo moved to position: {position}")
        sleep(delay)

    def run_demo(self):
        while True:
            # Move to ~50 degrees (around 0.3 value in gpiozero)
            self.move_to_position(0.3)
            # Move back to 0 degrees (center is 0)
            self.move_to_position(0.0)

if __name__ == "__main__":
    servo_controller = ServoController()
    servo_controller.run_demo()


    ##OLD CODE ##
# from gpiozero import Servo
# from time import sleep

# # Use GPIO16 (BCM mode) and adjust pulse width for microservo compatibility
# servo = Servo(16, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

# while True:
#     # Move to ~50 degrees (around 0.3 value in gpiozero)
#     servo.value = 0.3  
#     print("Servo moved to 50 degrees")
#     sleep(1)

#     # Move back to 0 degrees (center is 0)
#     servo.value = 0.0  
#     print("Servo moved to 0 degrees")
#     sleep(1)
