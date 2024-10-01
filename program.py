import serial
import time

ser = serial.Serial(
port='COM11',
baudrate=115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS
)



while(not ser.isOpen()):
    ser.open()
    time.sleep(1)



def checksum(data):
    length = int.to_bytes(len(data), byteorder='little')
    payload = length + data
    print(payload)
    cs = 0
    for i in payload:
        cs = cs ^ i
    return b'\xAA\x55' + payload + int.to_bytes(cs, byteorder='little')

ser.write(checksum(b'\x01\x04\x40\x06\x04\x00'))
