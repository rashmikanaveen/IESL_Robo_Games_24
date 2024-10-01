import serial
import time

# Open serial connection
ser = serial.Serial(
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Wait for the serial port to open (if needed)
while not ser.isOpen():
    ser.open()
    time.sleep(3)

# Function to calculate the checksum
def checksum(data):
    length = int.to_bytes(len(data), byteorder='little')
    payload = length + data
    print(payload)
    cs = 0
    for i in payload:
        cs = cs ^ i
    return b'\xAA\x55' + payload + int.to_bytes(cs, byteorder='little')

# Run the code for t seconds
start_time = time.time()
while time.time() - start_time < 1:
    # Send the data over the serial connection
    ser.write(checksum(b'\x01\x04\x40\x06\x04\x00'))
    
    # Add a delay to control how often data is sent (e.g., every second)
    time.sleep(1)

# Close the serial connection
ser.close()