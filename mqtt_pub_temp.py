import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from sense_hat import SenseHat
import logging
import time

logging.basicConfig()
sense = SenseHat()

mqtt_broker_ip = "10.0.2.174"
mqtt_broker_port = 1883
topic_sub = "sensors/poll"
topic_pub = "sensors/temp"

green = (0, 255, 0)
red = (255, 0, 0)
nothing = (0,0,0)

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

def publishing_1():
    G = green
    O = nothing
    upload = [
    O, O, O, O, O, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O, 
    O, G, G, G, G, G, G, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, O, O, O, O, O,
    ]
    return upload
    
def publishing_2():
    G = green
    O = nothing
    upload = [
    O, O, G, G, G, G, O, O, 
    O, G, G, G, G, G, G, O,
    O, O, O, G, G, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, G, G, O, O, O,
    ]
    return upload

def publishing_3():
    G = green
    O = nothing
    upload = [
    O, O, O, G, G, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O, 
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O,
    O, G, G, G, G, G, G, O,
    ]
    return upload
    
def publishing_4():
    G = green
    O = nothing
    upload = [
    O, O, O, G, G, O, O, O, 
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O, 
    O, O, O, G, G, O, O, O,
    O, O, G, G, G, G, O, O,
    O, G, G, G, G, G, G, O,
    O, O, O, G, G, O, O, O,
    O, O, O, G, G, O, O, O,
    ]
    return upload

def publish_animation():
    stages = [publishing_1, publishing_2, publishing_3, publishing_4]
    for i in range(0, 13):
        sense.set_pixels(stages[i % len(stages)]())
        time.sleep(0.25)

# the callback for when the client recieves a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc) + " and CONNACK " + mqtt.connack_string(rc))
    print("%s:%d" % (mqtt_broker_ip, mqtt_broker_port))
    
    # Subscribing in on_connect() means that if we lose the connection and reconnect,
    #  then subscriptions will be renewed
    #client.subscribe(topic_sub) # not sure I need this
    
# the callback for when a message is published
def on_publish(client, userdata, mid):
    print("published " + userdata + " mid " + mid)
    
def on_disconnect(client, userdata, rc):
    print("disconnected")
    
def c_to_f(c):
    return (c * (9/5)) + 32

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.loop_start()

sense.set_pixels(raspi_logo())
crc = client.connect(mqtt_broker_ip, mqtt_broker_port, 60)
print(mqtt.connack_string(crc))
time.sleep(5)
sense.clear()

while(True):
    rc = ""
    try:
        client.reconnect()
        
        temp = c_to_f(sense.get_temperature_from_pressure())
        print("\n%.2f" % temp)
        rc = publish.single(topic_pub, temp, qos=2, hostname=mqtt_broker_ip, port=mqtt_broker_port)
        publish_animation()
        print("sent")
        client.disconnect()
    except Exception as e:
        print("\n" + str(e))
        sense.set_pixels(not_connected())
    time.sleep(15)
    sense.clear()

#client.loop_forever()