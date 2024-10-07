import serial
import time
import logging

# Configure logging to help with debugging and monitoring
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_checksum(payload):
    """
    Calculate the checksum by XORing all bytes in the payload.

    Args:
        payload (bytes): The payload bytes.

    Returns:
        bytes: The checksum byte.
    """
    checksum = 0
    for byte in payload:
        checksum ^= byte
    return checksum.to_bytes(1, byteorder='little')

def create_drive_direct_command(left_velocity, right_velocity):
    """
    Create a Drive Direct command packet for the Kobuki.

    Args:
        left_velocity (int): Velocity for the left wheel (-32768 to 32767).
        right_velocity (int): Velocity for the right wheel (-32768 to 32767).

    Returns:
        bytes: The complete command packet.
    """
    # Header for Kobuki packets
    HEADER = b'\xAA\x55'

    # Packet Identifier for command packets
    PID = b'\x01'

    # Data Length: Number of bytes following (PID + Data Length + Command + Velocities)
    # For Drive Direct: PID (1) + Data Length (1) + Command (1) + Left Vel (2) + Right Vel (2) = 6 bytes
    DATA_LENGTH = b'\x06'

    # Command code for Drive Direct
    COMMAND = b'\x40'

    # Convert velocities to little-endian signed 16-bit integers
    left_vel_bytes = left_velocity.to_bytes(2, byteorder='little', signed=True)
    right_vel_bytes = right_velocity.to_bytes(2, byteorder='little', signed=True)

    # Assemble the payload
    payload = PID + DATA_LENGTH + COMMAND + left_vel_bytes + right_vel_bytes

    # Calculate checksum
    checksum = calculate_checksum(payload)

    # Complete packet
    packet = HEADER + payload + checksum

    return packet

def initialize_serial(port, baudrate=115200, timeout=1):
    """
    Initialize and return a serial connection.

    Args:
        port (str): Serial port (e.g., 'COM11' or '/dev/ttyUSB0').
        baudrate (int, optional): Baud rate. Defaults to 115200.
        timeout (int, optional): Read timeout in seconds. Defaults to 1.

    Returns:
        serial.Serial: The serial connection object.
    """
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=timeout
        )
        logging.info(f"Opened serial port: {port}")
        return ser
    except serial.SerialException as e:
        logging.error(f"Failed to open serial port {port}: {e}")
        raise

def rotate_kobuki(ser, rotation_speed, rotation_time):
    """
    Rotate the Kobuki robot in place.

    Args:
        ser (serial.Serial): The serial connection to Kobuki.
        rotation_speed (int): Speed of rotation (positive for clockwise, negative for counter-clockwise).
        rotation_time (float): Duration of rotation in seconds.
    """
    # Define velocities for rotation
    # To rotate clockwise: left wheel forward, right wheel backward
    # To rotate counter-clockwise: left wheel backward, right wheel forward
    left_velocity = rotation_speed
    right_velocity = -rotation_speed

    # Create the Drive Direct command packet
    command_packet = create_drive_direct_command(left_velocity, right_velocity)
    logging.info(f"Sending rotation command: {command_packet.hex()}")

    # Send the command
    ser.write(command_packet)

    # Log the action
    logging.info(f"Rotating {'clockwise' if rotation_speed > 0 else 'counter-clockwise'} for {rotation_time} seconds.")

    # Wait for the specified duration
    time.sleep(rotation_time)

    # Stop the robot by sending zero velocities
    stop_packet = create_drive_direct_command(0, 0)
    ser.write(stop_packet)
    logging.info("Sent stop command to Kobuki.")

def main():
    # Configuration
    SERIAL_PORT = 'COM11'  # Change this to your Kobuki's serial port
    ROTATION_SPEED = 500   # Adjust speed as needed (range: -32768 to 32767)
    ROTATION_TIME = 2      # Duration in seconds to rotate

    # Initialize serial connection
    try:
        ser = initialize_serial(SERIAL_PORT)
    except Exception as e:
        logging.error("Exiting program due to serial connection failure.")
        return

    # Ensure the serial port is open
    if not ser.is_open:
        try:
            ser.open()
            logging.info("Serial port opened successfully.")
        except serial.SerialException as e:
            logging.error(f"Failed to open serial port {SERIAL_PORT}: {e}")
            return

    try:
        # Perform rotation
        rotate_kobuki(ser, ROTATION_SPEED, ROTATION_TIME)
    except Exception as e:
        logging.error(f"An error occurred during rotation: {e}")
    finally:
        # Close the serial connection
        ser.close()
        logging.info("Closed serial connection.")

if __name__ == "__main__":
    main()
