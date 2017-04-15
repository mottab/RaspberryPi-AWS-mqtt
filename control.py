#!/usr/bin/python3

#Testing Amazon AWS IoT using RaspberryPi and Python...

#required import libraries

import sys
import ssl
import paho.mqtt.client as mqtt

# on_connect: called when client tries to connect to mqtt server
def on_connect(mqttc, obj, flags, rc):
	if rc == 0:
		print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
	elif rc == 1:
		print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")


#on_subscribe: called when topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))


#on_message: called when a message is received by a topic
def on_message(mqttc, obj, msg):
	print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))


#creating a client with client-id=mqtt-raspberrypi-test
mqttc = mqtt.Client(client_id="mqtt-raspberrypi-test")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set("/home/pi/deviceSDK/root-CA.pem",
                certfile="/home/pi/deviceSDK/24e7e8f626-certificate.pem.crt",
                keyfile="/home/pi/deviceSDK/24e7e8f626-private.pem.key",
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("a3maekzwcug08p.iot.us-east-1.amazonaws.com", port=8883) #AWS IoT service hostname and portno

#the topic to publish to
mqttc.subscribe("$aws/things/mqtt-listener/shadow/update/#", qos=1) #The names of these topics start with $aws/things/thingName/shadow."

#automatically handles reconnecting
mqttc.loop_forever()
