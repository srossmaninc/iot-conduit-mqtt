<h3>Overarching Objective</h3>
To publish/subscribe to MQTT topics sourced from direct MQTT-capable devices/a TTN MQTT server, and to implement visual indicators of data transfers/connectivity. In addition, the subscribing RPI node catalogs the received data into an InfluxDB database.
Implementation Details
<b>Mosquitto Broker:</b> a yellow “ripple” design to show that the Mosquitto broker is running successfully with a red “ripple” denoting that the broker is offline.

<b>RPI Publishing Node:</b> a green up arrow showing the node is connected to the broker with an “up scroll” animation on actual data upload. A red “X” is displayed if the node is offline or unable to reach the Mosquitto broker.

<b>RPI Subscribing Node:</b> a blue down arrow showing the node is connected to the broker with a “down scroll” animation on actual data reception. A red “X” is displayed if the node is offline or unable to reach the Mosquitto broker.

<h3>MQTT Broker</h3>
The Mosquitto broker is started using a bash script I wrote that automates the Python script that is run in addition to starting the actual broker service.

```
#! /bin/sh
sudo systemctl start mosquitto
python ~/Desktop/mqtt-broker-status.py
```

<h3>MQTT Publish/Subscribe</h3>
<h4>RPI publish node code</h4>

```
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from sense_hat import SenseHat
import logging
import socket
import time

# <---SENSE HAT // MQTT VARIABLES // LOGGING--->
logging.basicConfig()
sense = SenseHat()
sense.low_light = True

mqtt_broker_ip = "10.0.2.174"
mqtt_broker_port = 1883
topic_pub = "sensors/temp"

# <---COLORS--->
green = (0, 255, 0)
red = (255, 0, 0)
nothing = (0,0,0)

# <---ANIMATION & STAGES--->
def not_connected():

def raspi_logo():

def publishing_1():
    
def publishing_2():

def publishing_3():
    
def publishing_4():

def publish_animation():
    stages = [publishing_1, publishing_2, publishing_3, publishing_4]
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
sense.set_pixels(raspi_logo())
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
        sense.set_pixels(not_connected())
    time.sleep(60)
    sense.clear()
```

<h4>RPI subscribe node code</h4>

```
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

def raspi_logo():

def subscribing_1():

def subscribing_2():
    
def subscribing_3():
    
def subscribing_4():

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
```

<h3>InfluxDB & the TIG Stack (what is run on the subscription “hub” node)</h3>
The RPI subscription node’s Python script does not validate that the data was read into the InfluxDB database but rather solely displays the RPI node’s connectivity to the Mosquitto broker. The data is read into the database via the Telegraf configuration file.

```
# file is found at /home/tig-rpi/telegraf.conf
# # Read metrics from MQTT topic(s)
[[inputs.mqtt_consumer]]
servers = ["tcp://10.0.2.174:1883"]
topics = [
"sensors/temp",
]
qos = 2
```

While it does not communicate via our Mosquitto broker, we also draw our TTN data from the supplied TTN MQTT broker in the same configuration file.

```
# file is found at /home/tig-rpi/telegraf.conf
[[inputs.mqtt_consumer]]
  alias = "thing_network_consumer"
  name_override = "thing_network"
  servers = ["tcp://nam1.cloud.thethings.network:1883"]
  topics = ["#"]
  max_undelivered_messages = 1

    username = "$THING_USERNAME"
    password = "$THING_API_KEY" 
    data_format = "json_v2"

  [[inputs.mqtt_consumer.json_v2]]
    [[inputs.mqtt_consumer.json_v2.tag]]
    path = "@this.end_device_ids.device_id"

  [[inputs.mqtt_consumer.json_v2.object]]
    path = "end_device_ids"
    disable_prepend_keys = true

  [[inputs.mqtt_consumer.json_v2.object]]
    path = "uplink_message"
    disable_prepend_keys = true
    excluded_keys = ["time", "timestamp"]

  [[inputs.mqtt_consumer.json_v2.object]]
    path = "uplink_message.rx_metadata"
    disable_prepend_keys = true
    excluded_keys = ["time", "timestamp"]

# data thang
[[inputs.mqtt_consumer]]
alias = "thing_network_consumer2"
name_override = "sensor_data"

  servers = ["tcp://nam1.cloud.thethings.network:1883"]
  topics = ["#"]

  username = "$THING_USERNAME"
  password = "$THING_API_KEY" 
  data_format = "json_v2"

 [[inputs.mqtt_consumer.json_v2]]
 [[inputs.mqtt_consumer.json_v2.object]]
  path = "@this.uplink_message.decoded_payload"
  disable_prepend_keys = true
```

I coded a basic bash script that will automatically configure and start all the required TIG stack services that need to be run at startup.

```
#! /bin/sh
echo "exporting telegraf API key"
export INFLUX_TOKEN=BAuKR5TW0Cb21uuGilS3OYmvhNInWeYN7blIsj2135iVFKVx4FMgho0hgxAYxWc_WnJfKgvukxIdUWp0ImW02g==

echo "exporting ttn username"
export THING_USERNAME=feather-test-01@ttn
echo $THING_USERNAME

echo "exporting ttn api key {feather test}"
export THING_API_KEY="key!"
echo $THING_API_KEY

echo "starting telegraf with key " $INFLUX_TOKEN
telegraf --debug --config /home/tig-rpi/telegraf.conf

sudo systemctl start influxdb
```

<h3>Example</h3>
[INSERT EXAMPLE HERE]
