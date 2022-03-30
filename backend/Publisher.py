import argparse, threading, time, random
import json

import paho.mqtt.client as mqtt

class Publisher():
    def __init__(self, args=None):
        if args:
            self.port = args["port"]
            self.ip = args["ip"]
            # self.topics = args["topic"]
        else:
            self.port = 1883
            self.ip = "localhost"
            # self.topics = ['brightness']
        
        self.client = mqtt.Client()
        

    def publish(self, topic, data):
        # Establish connection to mqtt broker
        self.client.connect(host=self.ip, port=self.port)
        payload = json.dumps(data).encode()
        self.client.publish(topic=topic, payload=payload)
        
    
    def main(self):
        index = 0
        # Intervally send topic message
        try:
            while True:
                if (index %2 == 0):
                    # if 'brightness' in self.topics:
                    payloads = [
                    {
                        "from": 1,
                        "data": 28 + random.random()*0.2,
                        "type": "temperature"
                    },
                    {
                        "from": 1,
                        "data": 8 + random.random()*0.6,
                        "type": "humidity"
                    },
                    ]
                else :
                    payloads = [
                    {
                        "from": 1,
                        "data": 27 + random.random()*1.4,
                        "type": "temperature"
                    },
                    {
                        "from": 1,
                        "data": 8 + random.random()*0.4,
                        "type": "humidity"
                    },
                    ]
                for payload in payloads:
                    self.publish("sensor", payload)
                    print("Payload send: %s" % str(payload))
                # payload = {"to": 1, "brightness": 32}
                # self.publish("lights", payload)
                # print("Payload send: %s" % str(payload))
                time.sleep(1)
                index += 1
        
        except KeyboardInterrupt as e:
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
    parser.add_argument("--topic",
                        default="brightness",
                        choices=['brightness'],
                        nargs="+",
                        help="Available information to publish")
    args = vars(parser.parse_args())
    publisher = Publisher(args)
    publisher.main()