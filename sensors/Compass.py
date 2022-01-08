#!/usr/bin/python3
import time
import serial

print("UART Demonstration Program")
print("NVIDIA Jetson Nano Developer Kit")

try:
    serial_port = serial.Serial(
        port="/dev/ttyACM1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    )
    # Wait a second to let the port initialize
    time.sleep(1)
except:
    serial_port = None

class Compass:
    def __init__(self):
        self.bearing = 0
        self.azimuth = 0

    def update(self, data):
        data = data.split(": ")
        # print(data)
        if data[0] == " Bearing":
            self.bearing = int(data[1][:-2])
        elif data[0] == " Azimuth":
            self.azimuth = int(data[1][:-2])
        
    def getCompass(self):
        print("Azimuth: {}, Bearing: {}".format(self.azimuth, self.bearing))
        
        return {
            "bearing":self.bearing, 
            "azimuth":self.azimuth,
            }
            
myCompass = Compass()

def compass_read():
    try:
        # Send a simple header
        if serial_port.inWaiting():
            while serial_port.inWaiting():
            # for _ in range(5):
                data = serial_port.readline()
                myCompass.update(data=data.decode())
            
            return myCompass.getCompass()
    except KeyboardInterrupt:
        print("Exiting Program")

    except Exception as exception_error:
        print("Error occurred. Exiting Program")
        print("Error: " + str(exception_error))
    
    return {}

def compass_close():
    serial_port.close()

if __name__ == "__main__":
    while True:
        compass_read()
        time.sleep(1)
