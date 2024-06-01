import MCP3202, os
from time import sleep
import math
import Adafruit_DHT
import RPi.GPIO as gpio
import paho.mqtt.client as paho
import telepot
from telepot.loop import MessageLoop

Aman_id=******
bot = telepot.Bot('1023574477:AAFDMgn1TBpBG******qHya3b2IHPT1kg')
DHT_SENSOR = Adafruit_DHT.DHT11
gpio = 5

broker="10.42.0.1" #ip broker
port=1883

def translate(value,leftMin,leftMax,rightMin,rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

try:
    while True:
        os.system("clear")
        value1 = MCP3202.readADC(0)
        map = translate(value1, 0, 1023, 0, 100)    
        output = map * 3.3 / 100
        output = (133.42*output*output*output - 255.86*output*output + 857.39*output)/2
        tds = str(math.trunc(output))
        print(tds +" ppm")
                
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, gpio)

        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        else:
            print("Failed to retrieve data from humidity sensor")
            
        
        client1= paho.Client("suhu")                           #create client object
        client1.on_publish = on_publish                          #assign function to callback
        client1.connect(broker,port)                                 #establish connection
        ret= client1.publish("temp",temperature)                   #publish
        ret= client1.publish("hum", humidity)
        ret= client1.publish("tds", tds)
        
        tdsnilai = output
        if temperature > 30 :
            bot.sendMessage(Aman_id, 'hey! tanaman hidroponik mu kepanasan')
        elif tdsnilai > 1200 :
            bot.sendMessage(Aman_id, 'hey! tds tanaman hidroponik mu telah melebihi jumlah maksimal, segera tambahkan air')


        
except KeyboardInterrupt:
    print("bye")
