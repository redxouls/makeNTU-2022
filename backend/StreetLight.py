import time, copy

class StreetLight():
    def __init__(self, index):
        self.index = index
        self.warning_timer = time.time()
        self.lumos_timer = time.time()
        self.lumos_period = 5
        self.warning_period = 5
        self.mode = "default"
        self.payload = {
                        "to": index,
                        'brightness':26,
                
                    }
        self.default_light = {
                        "to": index,
                        'brightness':26,
                    }

    def set_default_brightness(self, brightness_percent):
        self.payload["brightness"] = self.payload["brightness"] * brightness_percent /100

    def lumos(self):
        self.mode = "lumos"
        self.lumos_timer = time.time()

    def fall(self):
        self.mode = "fall"
        self.warning_timer = time.time()

    
    def update(self, lightness):
        if self.mode == "default":
            self.default_light['brightness'] =  26 - round(lightness * 26 / 200)
            self.payload = copy.deepcopy(self.default_light)
        elif self.mode == "fall":
            self.default_light['brightness'] = 255
        elif self.mode == "lumos":
            self.default_light['brightness'] = 26
            
        if (time.time() - self.lumos_timer > self.lumos_period or time.time() - self.warning_timer > self.warning_period):
            self.mode = "default"
