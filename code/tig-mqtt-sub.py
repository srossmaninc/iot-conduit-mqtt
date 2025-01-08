import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import sense_shared as sym
import yaml
import time

# <---LOAD CONFIG YAML--->
with open('config.yaml', 'r') as file:
    config = yaml.load(file)

# <---SENSE HAT & MQTT VARIABLES--->
sense = SenseHat()
sense.low_light = True

mqtt_broker_ip = config['mqtt']['ip']
mqtt_broker_port = config['mqtt']['port']
topic_sub = config['mqtt']['topic']

def subscribe_animation():
    stages = sym.sub_stages
    for i in range(0, 13):
        sense.set_pixels(stages[i % len(stages)]())
        time.sleep(0.25)

# <---CALLBACKS--->
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print("please note that this polls mqtt messages but does NOT verify\nthat the data was saved in InfluxDB via Telegraf")
    print("%s:%d" % (mqtt_broker_ip, mqtt_broker_port))
    # this will provide redundancy as if/when the connection is lost and renewed we will re-subscribe automatically
    client.subscribe(topic_sub)
    sense.clear()
    
def on_disconnect(client, userdata, rc):
    print("disconnected")
    sense.set_pixels(sym.no_connect)
    
def on_message(client, userdata, msg):
    print("message '%s'\n\thas been recieved successfully" % msg.payload)
    subscribe_animation()

# <---MQTT SETUP--->
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# <---DISPLAY LOGO--->
sense.set_pixels(sym.logo)
time.sleep(5)
sense.clear()

# <---AUTOMATICALLY RECONNECT/CONNECT--->
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)
client.loop_forever()
