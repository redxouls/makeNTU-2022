import argparse, threading, time
import json

import paho.mqtt.client as mqtt

from GPS import gps_read, gps_close
from Compass import compass_read, compass_close


class Publisher():
    def __init__(self, args):
        self.port = args["port"]
        self.ip = args["ip"]
        self.client = mqtt.Client()

    def publish(self, topic, data):
        payload = json.dumps(data).encode()
        self.client.publish(topic=topic, payload=payload)

    def gps_sensor(self):
        data = []
        while True:
            data = gps_read()
            if len(data) == 0:
                continue
            elif data[0] == 0:
                continue
            self.publish("gps", data)
            
    def compass_sensor(self):
        data = {}
        while True:
            data = compass_read()
            if len(data) == 0:
                continue
            self.publish("compass", data)
            time.sleep(0.05)

        
    def main(self):
        # Establish connection to mqtt broker
        self.client.connect(host=self.ip, port=self.port)
        self.client.loop_start()
        
        # Intervally send topic message
        try:
            t1 = threading.Thread(target=self.gps_sensor)
            t1.start()
        
            # t2 = threading.Thread(target=self.compass_sensor)
            # t2.start()
        
        except KeyboardInterrupt as e:
            gps_close()
            compass_close()
            self.client.loop_stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    
    args = vars(parser.parse_args())
    publisher = Publisher(args)
    publisher.main()
