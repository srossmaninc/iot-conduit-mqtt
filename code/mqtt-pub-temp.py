import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from sense_hat import SenseHat
import sense_shared as sym
import yaml
import logging
import socket
import time

# <---LOAD CONFIG YAML--->
with open('config.yaml', 'r') as file:
    config = yaml.load(file)

# <---SENSE HAT // MQTT VARIABLES // LOGGING--->
logging.basicConfig()
sense = SenseHat()
sense.low_light = True

mqtt_broker_ip = config['mqtt']['ip']
mqtt_broker_port = config['mqtt']['port']
topic_pub = config['mqtt']['topic']

def publish_animation():
    stages = sym.pub_stages
    for i in range(0, 13):
        sense.set_pixels(stages[i % len(stages)]())
        time.sleep(0.25)

# <---CALLBACKS & TEMP--->
# the callback for when the client recieves a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc) + " and CONNACK " + mqtt.connack_string(rc))
    print("%s:%d" % (mqtt_broker_ip, mqtt_broker_port))
    # Subscribing in on_connect() means that if we lose the connection and reconnect,
    #  then subscriptions will be renewed
    
# the callback for when a message is published
def on_publish(client, userdata, mid):
    print("published " + userdata + " mid " + mid)
    
def on_disconnect(client, userdata, rc):
    print("disconnected")
    
def c_to_f(c):
    return (c * (9/5)) + 32

# <---MQTT SETUP--->
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.loop_start()

# <---DISPLAY LOGO & INITIAL CONNECT--->
sense.set_pixels(sym.logo)
crc = client.connect(mqtt_broker_ip, mqtt_broker_port, 60)
print(mqtt.connack_string(crc))
time.sleep(5)
sense.clear()

# <---MAIN LOGIC--->
while(True):
    rc = ""
    try:
        client.reconnect()
        
        temp = c_to_f(sense.get_temperature_from_pressure())
        print("\n%.2f" % temp)
        influx_line_protocol = "temperature,hostname=" + socket.gethostname() + " temp=" + str(temp) + " "
        print(influx_line_protocol)
        rc = publish.single(topic_pub, influx_line_protocol, qos=2, hostname=mqtt_broker_ip, port=mqtt_broker_port)
        publish_animation()
        print("sent")
        
        client.disconnect()
    except Exception as e:
        print("\n" + str(e))
        sense.set_pixels(sym.no_connect)
    time.sleep(60)
    sense.clear()