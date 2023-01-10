import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import time

# <---SENSE HAT & MQTT VARIABLES--->
sense = SenseHat()
sense.low_light = True

mqtt_broker_ip = "10.0.2.174"
mqtt_broker_port = 1883
topic_sub = "sensors/temp"

# <---COLORS--->
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
nothing = (0,0,0)


# <---ANIMATION & STAGES--->
def not_connected():
    O = nothing
    R = red
    no_connect = [
    O, O, O, O, O, O, O, O,
    O, R, R, O, O, R, R, O,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, R, R, R, R, O, O,
    O, R, R, R, R, R, R, O,
    O, R, R, O, O, R, R, O,
    O, O, O, O, O, O, O, O,
    ]
    return no_connect

def raspi_logo():
    G = green
    R = red
    O = nothing
    logo = [
    O, G, G, O, O, G, G, O, 
    O, O, G, G, G, G, O, O,
    O, O, R, R, R, R, O, O, 
    O, R, R, R, R, R, R, O,
    R, R, R, R, R, R, R, R,
    R, R, R, R, R, R, R, R,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    ]
    return logo

def subscribing_1():
    B = blue
    O = nothing
    sub = [
    O, O, O, O, O, O, O, O, 
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, B, B, B, B, B, B, O,
    O, O, B, B, B, B, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return sub

def subscribing_2():
    B = blue
    O = nothing
    sub = [
    O, O, O, B, B, O, O, O, 
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, B, B, B, B, B, B, O,
    O, O, B, B, B, B, O, O,
    ]
    return sub
    
def subscribing_3():
    B = blue
    O = nothing
    sub = [
    O, B, B, B, B, B, B, O, 
    O, O, B, B, B, B, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, B, B, O, O, O,
    ]
    return sub
    
def subscribing_4():
    B = blue
    O = nothing
    sub = [
    O, O, O, B, B, O, O, O, 
    O, O, O, B, B, O, O, O,
    O, B, B, B, B, B, B, O,
    O, O, B, B, B, B, O, O,
    O, O, O, B, B, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
    ]
    return sub

def subscribe_animation():
    stages = [subscribing_1, subscribing_2, subscribing_3, subscribing_4]
    for i in range(0, 13):
        sense.set_pixels(stages[i % len(stages)]())
        time.sleep(0.25)

# <---CALLBACKS--->
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print("please note that this polls mqtt messages but does NOT verify\nthat the data was saved in InfluxDB via Telegraf")
    print("%s:%d" % (mqtt_broker_ip, mqtt_broker_port))
    # this will provide redundancy as if/when the connection is lost and renewed we will re-subscribe automatically
    client.subscribe("sensors/temp")
    sense.clear()
    
def on_disconnect(client, userdata, rc):
    print("disconnected")
    sense.set_pixels(not_connected())
    
def on_message(client, userdata, msg):
    print("message '%s'\n\thas been recieved successfully" % msg.payload)
    subscribe_animation()

# <---MQTT SETUP--->
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# <---DISPLAY LOGO--->
sense.set_pixels(raspi_logo())
time.sleep(5)
sense.clear()

# <---AUTOMATICALLY RECONNECT/CONNECT--->
client.connect(mqtt_broker_ip, mqtt_broker_port, 60)
client.loop_forever()
