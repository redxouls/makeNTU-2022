import argparse, threading, time
import json

import paho.mqtt.client as mqtt

class Publisher():
    def __init__(self, args=None):
        if args:
            self.port = args["port"]
            self.ip = args["ip"]
            self.topics = args["topic"]
        else:
            self.port = 1883
            self.ip = "localhost"
            self.topics = ['brightness']
        
        self.client = mqtt.Client()
        

    def publish(self, topic, data):
        # Establish connection to mqtt broker
        self.client.connect(host=self.ip, port=self.port)
        self.client.loop_start()
        payload = json.dumps(data).encode()
        self.client.publish(topic=topic, payload=payload)
    
    def main(self):
        
        # Intervally send topic message
        try:
            while True:
                if 'brightness' in self.topics:
                    payload = {
                        "to": 1,
                        "value": 10
                    }
                    self.publish("brightness", payload)
                    print("Payload send: %s" % str(payload))
                    time.sleep(1)
        
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