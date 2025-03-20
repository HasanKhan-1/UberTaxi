import RPi.GPIO as GPIO
import time

in1 = 17
in2 = 27
in3 = 4
in4 = 3

en1 = 24 # for forwards for speed
en2 = 38 # for forwards for speed
en1b = 25 # backwards for speed
en2b = 36 # backwards for speed
# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)

# Initialize PWM for speed control
pwm1 = GPIO.PWM(en1, 100)  # 100 Hz frequency
pwm2 = GPIO.PWM(en2, 100)  # 100 Hz frequency

# Start PWM with 0% duty cycle (motor stopped)
pwm1.start(0)
pwm2.start(0)

def stop_motors():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

def move_forward(speed):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)

if __name__ == "__main__":
    try:
        stop_motors()
        while True:
            move_forward(100)  # Move forward with 100% speed
            time.sleep(5)  # Move forward for 5 seconds
            stop_motors()
            time.sleep(2)  # Stop for 2 seconds
    except KeyboardInterrupt:
        pass
    finally:
        stop_motors()
        GPIO.cleanup()