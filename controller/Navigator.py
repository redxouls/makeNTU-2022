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

        url = "https://api.mapbox.com/directions/v5/mapbox/cycling/%6f,%6f;%6f,%6f?alternatives=false&continue_straight=true&geometries=geojson&language=en&overview=simplified&steps=true&access_token=pk.eyJ1IjoicmVkeG91bHMiLCJhIjoiY2t4N2R1Nm1uMHl4aTJwcXViYno1Ym9sNCJ9.fByzZrach_1gQlboB02hCg" % (o_long, o_lat, d_long, d_lat)
        res = requests.get(url)
        routes = res.json().get('routes')[0]

        # with open("routes.json", "r") as f:
        #     routes = json.loads(f.read()).get('routes')[0]

        steps = routes.get('legs')[0].get('steps')
        # print(steps)
        self.mode = "straight"
        for step in steps:
            maneuver =  step.get('maneuver')
            step_type = maneuver.get('type')
            duration = step.get('duration')
            if step_type == 'depart':
                print(step_type, duration)
                if duration > 10:
                    self.mode = "straight"
                    return 
            if step_type == 'turn':
                modifier = maneuver.get('modifier')
                print(step_type, modifier)
                self.mode = modifier
                return

    def setOrigin(self, origin):
        self.origin = origin

    def setDestination(self, destination):
        self.destination = destination
        
    def navigate(self):
        self.started = True
        while self.started:
            newOrigin = self.subscriber.data.get("gps", [121.543764, 25.019388])
            self.setOrigin(newOrigin)
            self.get_route()
            if self.serial_port:
                if self.mode == "left":
                    self.serial_port.write(b"1")
                    time.sleep(1)
                    self.serial_port.write(b"6")

                elif self.mode == "slight left":
                    self.serial_port.write(b"2")
                    time.sleep(1)
                    self.serial_port.write(b"7")

                elif self.mode == "straight":
                    self.serial_port.write(b"3")
                    time.sleep(1)
                    self.serial_port.write(b"8")
                
                elif self.mode == "slight right":
                    self.serial_port.write(b"4")
                    time.sleep(1)
                    self.serial_port.write(b"9")
                
                elif self.mode == "right":
                    self.serial_port.write(b"5")
                    time.sleep(1)
                    self.serial_port.write(b"0")
                print(self.mode)
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
