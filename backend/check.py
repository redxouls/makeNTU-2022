import argparse, json, time, datetime
import paho.mqtt.client as mqtt

class Subscriber():
    def __init__(self, args=None):
        self.client = mqtt.Client()
        self.topic_list = ["sensor", "noResponse"]
        self.data = {}
        self.data_limit = 10
        self.ip = args.get("ip", "localhost")
        self.port = args.get("port", 1883)

    def on_message(self, client, obj, msg):
        if msg.topic in self.topic_list:
            if msg.topic == "sensor":
                raw = json.loads(msg.payload.decode())
                msg_from = raw.get("from")
                msg_type = raw.get("type")
                msg_data = raw.get("data")
                if (msg_from not in self.data):
                    self.data[msg_from] = {}
                if (msg_type not in self.data[msg_from]):
                    self.data[msg_from][msg_type] = []
                
                self.data[msg_from][msg_type].append({
                    "time": '{0:%H:%M:%S}'.format(datetime.datetime.now()),
                    msg_type: msg_data
                })
                if len(self.data[msg_from][msg_type]) > self.data_limit:
                    self.data[msg_from][msg_type].pop(0)
        print(f"TOPIC: {msg.topic}, VALUE: {msg.payload}")
        

    def main(self):
        # Establish connection to mqtt broker
        self.client.on_message = self.on_message
        self.client.connect(host=self.ip, port=self.port)
        for t in self.topic_list:
            self.client.subscribe(t, 0)

        self.client.subscribe('lights', 0)

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
    subscriber = Subscriber(args)
    subscriber.main()