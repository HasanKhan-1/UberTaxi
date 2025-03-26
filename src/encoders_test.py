from gpiozero import RotaryEncoder
from signal import pause

class EncoderTracking:
    def __init__(self, encoder1_pins=(20, 21), encoder2_pins=(10, 9)):
        self.encoder1 = RotaryEncoder(a=encoder1_pins[0], b=encoder1_pins[1], max_steps=0)
        self.encoder2 = RotaryEncoder(a=encoder2_pins[0], b=encoder2_pins[1], max_steps=0)

        # Attach event handlers
        self.encoder1.when_rotated = self.update_encoders
        self.encoder2.when_rotated = self.update_encoders
    
    def update_encoders(self):
        print(f"Left Encoder: {self.encoder1.steps}, Right Encoder: {self.encoder2.steps}")

    def run_encoder(self):
        print("Encoders are running... Press Ctrl+C to exit.")
        pause()

# Example usage
if __name__ == "__main__":
    # Create an instance of EncoderTracking with default pins
    encoder_tracker = EncoderTracking()

        ##  specify custom pins if we want to ##
    # encoder_tracker = EncoderTracking(encoder1_pins=(5, 6), encoder2_pins=(13, 19))

    encoder_tracker.run_encoder()


    
        
    ## Tested Code that works! ##
# from gpiozero import RotaryEncoder
# from signal import pause

# # Define encoder objects
# encoder1 = RotaryEncoder(a=20, b=21, max_steps=0)  # Left Encoder
# encoder2 = RotaryEncoder(a=10, b=9, max_steps=0)  # Right Encoder

# def update_encoders():
#     print(f"Left Encoder: {encoder1.steps}, Right Encoder: {encoder2.steps}")

# # Monitor encoder values
# encoder1.when_rotated = update_encoders
# encoder2.when_rotated = update_encoders

# print("Encoders are running... Press Ctrl+C to exit.")
# pause()

