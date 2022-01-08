#!/usr/bin/python3
import time
import serial
import requests

class Navigator:
    def __init__(self, origin=[121.543764, 25.019388], destination=[121.534337, 25.019064], serial_port=None, subscriber=None):
        self.origin = origin
        self.destination = destination
        self.serial_port = serial_port
        self.subscriber = subscriber
        self.started = False
    
    def get_route(self):
        o_long, o_lat = self.origin
        d_long, d_lat = self.destination
        # origin_destination = "%6f,%6f;%6f,%6f" % (o_long, o_lat, d_long, d_lat)
        
        url = "https://api.mapbox.com/directions/v5/mapbox/cycling/%6f,%6f;%6f,%6f?alternatives=false&continue_straight=true&geometries=geojson&language=en&overview=simplified&steps=true&access_token=pk.eyJ1IjoicmVkeG91bHMiLCJhIjoiY2t4N2R1Nm1uMHl4aTJwcXViYno1Ym9sNCJ9.fByzZrach_1gQlboB02hCg" % (o_long, o_lat, d_long, d_lat)

        res = requests.get(url)
        routes = res.json().get('routes')[0]
        steps = routes.get('legs')[0].get('steps')
        
        for step in steps:
            step_type = step.get('maneuver').get('type')
            print(step_type)
            if step_type == "turn":
                print(step.get('maneuver').get('modifier'))
                return step.get('maneuver').get('modifier')

    def setOrigin(self, origin):
        self.origin = origin

    def setDestination(self, destination):
        self.destination = destination
        
    def navigate(self):
        self.started = True
        while self.started:
            newOrigin = self.subscriber.data.get("gps", [121.543764, 25.019388])
            self.setOrigin(newOrigin)
            direction = self.get_route()
            if self.serial_port:
                if "left" in direction:
                    self.serial_port.write(b"L")
                elif "right" in direction:
                    self.serial_port.write(b"R")
            
            time.sleep(1)

    def stop(self):
        self.started = False

if __name__ == "__main__":
    origin = [121.543764, 25.019388]
    destination = [121.534337, 25.019064]
    
    current = time.time()
    navigator = Navigator(origin, destination)
    for i in range(10):
        navigator.navigate()
        print(time.time()-current)
# try:
#     # Send a simple header
#     serial_port.write("UART Demonstration Program\r\n".encode())
#     serial_port.write("NVIDIA Jetson Nano Developer Kit\r\n".encode())
#     serial_port.write(b"L")
#     print("Sent")

# except KeyboardInterrupt:
#     print("Exiting Program")

# except Exception as exception_error:
#     print("Error occurred. Exiting Program")
#     print("Error: " + str(exception_error))

# finally:
#     serial_port.close()
#     pass
