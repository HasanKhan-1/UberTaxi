import smbus
import time

# I2C address of the Arduino
I2C_ADDRESS = 0x08

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_encoders():
    """Read encoder values from the Arduino."""
    try:
        # Read 4 bytes from the Arduino (2 bytes for each encoder)
        data = bus.read_i2c_block_data(I2C_ADDRESS, 0, 4)
        encoder1 = data[0] | (data[1] << 8)
        encoder2 = data[2] | (data[3] << 8)
        return encoder1, encoder2
    except OSError as e:
        print(f"Error reading from I2C: {e}")
        return None, None

if __name__ == "__main__":
    try:
        while True:
            encoder1, encoder2 = read_encoders()
            if encoder1 is not None and encoder2 is not None:
                print(f"Encoder 1: {encoder1}, Encoder 2: {encoder2}")
            time.sleep(1)
    except KeyboardInterrupt:
        pass