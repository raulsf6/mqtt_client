import sys
import signal
from argparse import ArgumentParser
import paho.mqtt.client as mqtt


def signal_handler(sig, frame):
    print('CTRL + C : Disconnecting from broker')
    client.disconnect()
    sys.exit(0)

argp = ArgumentParser(
    description="MQTT client that subscribes to specified host and topic",
    usage="mqtt.py [-o host] [-t topic] [-p port] [-l] [--list]"
)

topics = {}

argp.add_argument('-o', dest='host', help='Set the host', required=True)
argp.add_argument('-p', dest='port', default="1883", type=int, help='Set the port, default is 1883')
argp.add_argument('-q', dest='qos', default=0, choices=[0, 1, 2], type=int, help='Set the QoS, default is 0')
# argp.add_mutually_exclusive_group()
argp.add_argument('-l', '--list', dest='list', default=False, action='store_true', help='Catch and list server topics')
argp.add_argument('-t', dest='topic', help='Set the topic', default='$SYS/#')
argp.add_argument('--max-topics', dest='max_topics', help='Max topics to list', default=10, type=int)
args = argp.parse_args()

def on_connect(client, userdata, flags, rc):
    print("Connected with code " + str(rc))
    
    if (args.list):
        client.subscribe('#', qos=args.qos)
    else:
        client.subscribe(args.topic, qos=args.qos)

def on_message(client, userdata, msg):
    if (args.list):
        topics[msg.topic] = topics.get(msg.topic, 0) + 1
        if (len(topics) >= args.max_topics):
            for key, value in topics.items():
                print('Topic: ' + key + ' Freq: ' + str(value))
            client.disconnect()
            sys.exit(0)

    else:
        print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Trying to connect to " + args.host)
client.connect(args.host, args.port, 60)

signal.signal(signal.SIGINT, signal_handler)

client.loop_forever()

