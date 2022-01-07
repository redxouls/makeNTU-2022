import argparse, json
import paho.mqtt.client as mqtt


class Subscriber():
    def __init__(self, args=None):
        self.client = mqtt.Client()
        self.data = dict()
        self.ip = "localhost"
        self.port = 1883
        if args:
            self.ip = args.ip
            self.port = args.port

    def on_message(self, client, obj, msg):
        self.data[msg.topic] = json.loads(msg.payload.decode())
        print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
        print(self.data)

    def main(self):
        # Establish connection to mqtt broker
        
        self.client.on_message = self.on_message
        self.client.connect(host=self.ip, port=self.port)
        self.client.subscribe('gps', 0)
        self.client.subscribe('compass', 0)

        try:
            self.client.loop_forever()
        except KeyboardInterrupt as e:
            pass

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
    subscriber = Subscriber()
    subscriber.main(args)
