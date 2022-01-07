import argparse, threading, time
import json

import paho.mqtt.client as mqtt

from GPS import gps_read, gps_close
from Compass import compass_read, compass_close

def publish(client, topic, data):
    payload = json.dumps(data).encode()
    client.publish(topic=topic, payload=payload)

def gps_sensor(client):
    data = []
    while True:
        data = gps_read()
        if len(data) == 0:
            continue
        publish(client, "gps", data)
        
def compass_sensor(client):
    data = {}
    while True:
        data = compass_read()
        if len(data) == 0:
            continue
        publish(client, "compass", data)

        
def main(args):
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.connect(host=args['ip'], port=args['port'])
    client.loop_start()
    
    # Intervally send topic message
    try:
        t1 = threading.Thread(target=gps_sensor, args=(client,))
        t1.start()
    
        t2 = threading.Thread(target=compass_sensor, args=(client,))
        t2.start()
    
    except KeyboardInterrupt as e:
        gps_close()
        compass_close()
        client.loop_stop()


  
    
    


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
                        default="cpu",
                        choices=['cpu', 'mem', 'gps'],
                        help="Availabel information to publish")
    args = vars(parser.parse_args())
    main(args)
