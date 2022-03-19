/*
subscription
{
    "to": 1,
    "data": 30
}
*/

/*
publish
{
  "from": 1,
  "type": "temperature",
  "data": 26
}
*/


#define ID (1)
#define SEND_PERIOD 5000

#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>

// const char* ssid = "MakeNTU2022-A-2.4G";
// const char* password = "sustainable";

const char* ssid = "AndroidAPCB5F";
const char* password = "cljv7137";
const char* mqtt_server = "192.168.235.63";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (500)

// data
int temp;
int hum;
int PM25;
int distance;

bool getTemp;
bool getHum;
bool getPM25;
bool getDis;

void goodSensor(char* type, int data) {
  char sendMsg[MSG_BUFFER_SIZE];
  snprintf (sendMsg, MSG_BUFFER_SIZE, "{ \"from\": %d, \"type\": \" %s \", \"data\": %d}", ID, type, data);
  client.publish("sensor", sendMsg);
  Serial.print("[good Sensor] ");
  Serial.println(sendMsg);
}

void badSensor(char* type) {
  char sendMsg[MSG_BUFFER_SIZE];
  snprintf (sendMsg, MSG_BUFFER_SIZE, "{ \"from\": %d, \"type\": \" %s \"}", ID, type);
  client.publish("noResponse", sendMsg);
  Serial.print("[bad Sensor] ");
  Serial.println(sendMsg);
}

void publish() {
  char snedMsg[MSG_BUFFER_SIZE];// = "{ \"from\": 1, \"type\": \"temperature\", \"data\": 26}";
  bool notReport = false;
  if (getTemp) {
    goodSensor("temperature", temp);
    getTemp = false;
  }
  else
    badSensor("temperature");
    
  if (getHum) {
    goodSensor("humidity", hum);
    getHum = false;
  }
  else
    badSensor("humidity");

  if (getPM25) {
    goodSensor("PM2.5", PM25);
    getPM25 = false;
  }
  else
    badSensor("PM2.5");
    
  if (getDis) {
    goodSensor("distance", distance);
    getDis = false;
  }
  else
    badSensor("distance");
}


void setup_wifi() {

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  char msg[MSG_BUFFER_SIZE];
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    msg[i] = (char)payload[i];
  }
  msg[length] = '\0';
  Serial.println();
  
  StaticJsonBuffer<300> JSONBuffer;                         //Memory pool
  JsonObject& parsed = JSONBuffer.parseObject(msg); //Parse message
  if (!parsed.success()) {   //Check for errors in parsing
    Serial.println("Parsing failed");
    return;
  }
  
//  {
//    "to": 1,
//    "data": 30
//  }
  int id = parsed["to"];
  if (id != ID)
    return;
  int lightness = parsed["data"];
  //Serial.println("light %d get lightness %d", id, lightness);
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
            client.publish("outTopic", "hello world");      
      // ... and resubscribe
      client.subscribe("brightness");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  //pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (Serial.available()) {
    String sensorType = Serial.readStringUntil(' ');
    int data = Serial.parseInt();
    if (sensorType == "t") {
      temp = data;
      getTemp = true;
    }
    if (sensorType == "h") {
      hum = data;
      getHum = true;
    }
    if (sensorType == "P") {
      PM25 = data;
      getPM25 = true;
    }
    if (sensorType == "d") {
      distance = data;
      getDis = true;
    }
  }
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  unsigned long now = millis();
  if (now - lastMsg > SEND_PERIOD) {
    lastMsg = now;
    publish();
  }
}
