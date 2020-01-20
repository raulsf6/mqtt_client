import sys
from argparse import ArgumentParser
import paho.mqtt.client as mqtt


argp = ArgumentParser(
	description="MQTT client that subscribes to specified host and topic",
	usage="mqtt.py [-o host] [-t target] [-p port]"
)

argp.add_argument('-o', dest='host', default="mqtt.eclipse.org", help='Set the host, default is mqtt.eclipse.org')
argp.add_argument('-t', dest='topic', default="$SYS/#", help='Set the topic, default is $SYS/#')
argp.add_argument('-p', dest='port', default="1883", help='Set the port, default is 1883')

args = argp.parse_args()

def on_connect(client, userdata, flags, rc):
	print("Connected with code" + str(rc))
	client.subscribe(args.topic)

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Trying to connect to " + args.host)
client.connect(args.host, int(args.port), 60)

client.loop_forever()
