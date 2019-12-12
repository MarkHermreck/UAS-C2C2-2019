"""
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
"""

import time, logging, sys, pyaudio, wave, os, time, test_audio_record
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from communication import Communication

# Connect to xBee
COM_CONNECTION_STRING = '/dev/ttyAMA0'      #potential option
com = Communication(COM_CONNECTION_STRING, 0.5)

#creating temperature log file
logFile = open("ISULogs.txt", "a+")
logFile.truncate(0);
logTime = time.time();
lastdetectTime = time.time();

#setting up RPI GPIO
GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir = 40 #Assign pin 8 to PIR
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

    logfile.write("Temperature data recorded @ " + timeString + " with a value of " + str(temperature) + " degrees Celsius \n")
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
    
def sendAudioFile(filetoSend):
    #hardcoded file format
    n_channels = 1
    sample_width = 2
    framerate = 44100
    n_frames = 204800
    comp_type = "NONE"
    comp_name = "not compressed"

    f = wave.open(filetoSend, "rb")
    
    bytesSent = 0
    lastBytesSent = 0
    f1 = f.readframes(n_frames)
    
    #send file
    for x in f1:
        com.sendAudio(bytes([x]))
        bytesSent = bytesSent + 1
        if bytesSent >= lastBytesSent + 1024:
            lastBytesSent = lastBytesSent + 1024
        
    #file sent
    f.close()


#infinitely looping function that checks the motion detector, logs a temperature value if it's been 5 minutes, and checks
#the radio for a ping from the drone
iteration = 0;

logTemperature(logFile)
logFile.close()

while True:
    logFile = open("ISULogs.txt", "a+")
    #radio check here, joe
    radioCheck = com.receive()
    if radioCheck == "Requesting ISU1 data":    #each box should probably have a different name (ISU1, ISU2)
        com.send("ISU1 Ready")                   #ping response
        print("received ping")
        time.sleep(1)
        com.send("SendingTemperatureFile")
        audioName = 'test' + str(iteration) + '.wav'
        sendTextFile("/home/pi/ISULogs.txt")  #find name of file
        com.send("EndOfFile")
        #com.send("SendingAudioFile")
        sendAudioFile("/home/pi/" + audioName) #still writing this
        #com.send("EndOfFile")

    if time.time() - logTime >= 300:
        logTemperature(logFile)
        logTime = time.time()

    if GPIO.input(pir):  # If PIR pin goes high, motion is detected
        if time.time() - lastdetectTime > 5:
            timeString = str(time.ctime(time.time()))
            logFile.write("Motion detected at @ " + timeString + " \n")
            print("Motion Detected!")
            test_audio_record.audio_record(iteration)  # call the audo_record program and excecute the audio_record function.
            iteration += 1
            
            lastdetectTime = time.time();
        else:
            print("Motion detected during audio record, aborting.")

    logFile.close()
