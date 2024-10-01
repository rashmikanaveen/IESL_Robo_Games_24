import serial
import time

# Open the serial connection
ser = serial.Serial(
    port='COM8',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Check if the serial connection is open, and if not, open it
while not ser.isOpen():
    ser.open()
    time.sleep(1)

# Define a checksum function
def checksum(data):
    length = int.to_bytes(len(data), byteorder='little')
    payload = length + data
    print("Payload:", payload)
    cs = 0
    for i in payload:
        cs = cs ^ i
    return b'\xAA\x55' + payload + int.to_bytes(cs, byteorder='little')

# Function to move the robot for a given duration
def move_robot(duration):
    # Convert the duration to milliseconds (assuming the robot accepts time in milliseconds)
    duration_ms = int(duration * 1000)  # Convert to milliseconds
    duration_bytes = duration_ms.to_bytes(2, byteorder='little')  # Convert to bytes (2 bytes for up to 65535ms)

    # Command structure (example) with duration added to payload
    command = b'\x01\x04\x40\x06\x04' + duration_bytes
    ser.write(checksum(command))
    print(f"Moving for {duration} seconds...")

# Set the moving duration (change this to the desired time in seconds)
move_duration = 5  # Change this value from 2 to 10 seconds as needed

# Call the move function
move_robot(move_duration)

# Optionally, you can add a delay to wait for the move to complete
time.sleep(move_duration)

# Close the serial connection after the movement
ser.close()
