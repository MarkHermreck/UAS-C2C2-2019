"""
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
"""

import time, logging, sys, temperusb, temper, PyAudio, wave, os, time, test_audio_record
import RPi.GPIO as GPIO
import time
from communication import Communication

# Connect to xBee
COM_CONNECTION_STRING = '/dev/ttyUSB1'      #potential option
com = Communication(COM_CONNECTION_STRING, 0.5)

#creating temperature log file
logFile = open("ISULogs.txt", "a+")
logFile.truncate(0);
logTime = time.time();
lastdetectTime = time.time();

#setting up RPI GPIO
GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir = 8 #Assign pin 8 to PIR
#led = 10 Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
print ("Motion detector initializing . . .")

"""
This function is called every 5 minutes and is responsible for pulling temperature data and appending it to the end
of the file created above in main. This will be placed in the temperature handler file, whenever that's done. Will also
need to adjust this function to have temperature variable be the value returned by the usb. 

Currently broken, waiting on temperature sensor to work.

Inputs: logFile, the txt file created earlier in the main function. 
"""
def logTemperature(logfile):
    timeString = str(time.ctime(time.time()))
    temperature = 0;
    #temperature stuff, should move to function
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4

    _, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    logfile.write("Temperature data recorded @ " + timeString + " with a value of " + str(temperature) + " degrees Celsius")
    return None;


"""
This function sends an entire text file over the Xbees.
Inputs: filetoSend, string value of entire name of file, including file extension.
"""
def sendTextFile(filetoSend):
    f = open(filetoSend, "r")
    f1 = f.readlines()
    for x in f1:
        com.send(x)
    f.close()
    # file sent, inform the receiver
    com.send("Text file sent.")



#infinitely looping function that checks the motion detector, logs a temperature value if it's been 5 minutes, and checks
#the radio for a ping from the drone
iteration = 0;
while True:

    #radio check here, joe
    radioCheck = com.receive()
    if radioCheck == "Requesting ISU1 data":    #each box should probably have a different name (ISU1, ISU2)
        com.send("ISU1Ready")                   #ping response
        time.sleep(1)
        com.send("SendingTemperatureFile")
        sendTextFile()  #find name of file
        com.send("EndOfFile")
        com.send("SendingAudioFile")
        sendAudioFile() #still writing this
        com.send("EndOfFile")

    if time.time() - logTime >= 300:
        logTemperature(logFile)
        logTime = time.time()

    if GPIO.input(pir):  # If PIR pin goes high, motion is detected
        if time.time() - lastdetectTime > 5:

            print("Motion Detected!")
            test_audio_record.audio_record(iteration)  # call the audo_record program and excecute the audio_record function.
            iteration += 1
            lastdetectTime = time.time();
        else:
            print("Motion detected during audio record, aborting.")


