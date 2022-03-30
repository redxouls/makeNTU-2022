import time, datetime, copy
from StreetLight import StreetLight

class LightController:
    def __init__(self, num_lights=8) -> None:
        self.num_lights = num_lights
        self.fall_warning = False
        self.warning_timer = time.time()
        self.warning_period = 5
        self.lumos_timer = [time.time() for i in range(8)]
        self.lumos_period = 5
        self.lumos_range = 2
        self.streetlights = [StreetLight(i) for i in range(num_lights)]
        self.fall_event = {}
    
    def change_brightness(self, index, brightness_percent):
        self.streetlights[index].set_default_brightness(brightness_percent)

    def fall(self, index, probability):
        if probability > 0.1:
            self.fall_event = {
                "fall": True,
                "time": time.time(),
                "timeString": '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()),
                "index": index,
                "probability": probability
            }
            for streetlight in self.streetlights:
                streetlight.fall()
        
    def lumos(self, index):
        for i in range(max(0, index - self.lumos_range), min(self.num_lights, index + self.lumos_range)):
            self.streetlights[i].lumos()

    def getStatus(self):
        print(self.fall_event)
        if self.fall_event.get("fall", False):
            payload = copy.deepcopy(self.fall_event)
            self.fall_event = {}
            return payload
        else:
            return {
                "fall": False
            }

    def update(self, publisher, subscriber):
        while True:
            lightness = 50
            if subscriber.data.get(0, False):
                lightnesses = subscriber.data[0].get(" lightness ", [])
                if (len(lightnesses)):
                    lightness = lightnesses[-1].get(" lightness ", 50)
            
            for streetlight in self.streetlights:
                    streetlight.update(lightness)
                    publisher.publish('lights', streetlight.payload)
                
            time.sleep(3)