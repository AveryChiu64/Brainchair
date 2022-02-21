import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import  time

broker="test.mosquitto.org"
broker="192.168.1.21"
#define callback
def on_message(client, userdata, message):
   msg=str(message.payload.decode("utf-8"))
   #print("message =",msg)
   topic=message.topic
   messages.append([topic,msg])
def on_connect(client, userdata, flags, rc):

    if rc==0:
        client.connected_flag=True
        client.subscribe(sub_topic)
    else:
        client.bad_connection_flag=True
        client.connected_flag=False



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
left_forward = 11
left_reverse = 13
right_forward = 15
right_reverse = 17
GPIO.setup(left_forward,GPIO.OUT)
GPIO.setup(left_reverse,GPIO.OUT)
GPIO.setup(right_forward,GPIO.OUT)
GPIO.setup(right_reverse,GPIO.OUT)

##MQTT
messages=[]
sub_topic="pi/GPIO/control/#"
client= mqtt.Client("GPIO-client-001")  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("house/bulb1","on")  
######
client.on_message=on_message
client.on_connect=on_connect
client.connected_flag=False
client.connect(broker)#connect
while True:
    client.loop(0.01)
    time.sleep(1)
    if len(messages)>0:
        m=messages.pop(0)
        print("received ",m)
        if m[1] == "left_forward":
            GPIO.output(left_forward,GPIO.HIGH)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
        elif m[1] == "left_reverse":
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.HIGH)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
        elif m[1] == "right_forward":
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.HIGH)
            GPIO.output(left_forward,GPIO.LOW)
        elif m[1] == "right_reverse":
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.HIGH)
        else:
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)
            GPIO.output(left_forward,GPIO.LOW)