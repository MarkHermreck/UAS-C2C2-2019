"""
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
"""

import time, logging, sys, temperusb, temper
from communication import Communication

# Connect to xBee
COM_CONNECTION_STRING = '/dev/ttyUSB1'      #potential option
com = Communication(COM_CONNECTION_STRING, 0.1)

#three things need to be done
#get temperature every X
#monitor

#creating data file
logFile = open("ISULogs.txt", "a+")
logFile.truncate(0);
logTime = time.time();



"""
This function is called every 5 minutes and is responsible for pulling temperature data and appending it to the end
of the file created above in main. This will be placed in the temperature handler file, whenever that's done. Will also
need to adjust this function to have temperature variable be the value returned by the usb
Inputs: logFile, the txt file created earlier in the main function. 
"""
def logTemperature(logfile):
    timeString = str(time.ctime(time.time()))
    temperature = 0;
    #temperature = temperatureHandler.get_temperatures();
    logfile.write("Temperature data recorded @ " + timeString + " with a value of " + str(temperature) + " degrees Celsius")
    return None;


"""
This function sends an entire file.
Inputs: filetoSend, string value of entire name of file, including file extension.
"""
def sendFile(filetoSend):
    f = open(filetoSend, "r")
    f1 = f.readlines()
    for x in f1:
        com.send(x)
    f.close()
    # file sent, inform the receiver
    com.send("File sent.")

while True:
    if time.time() - logTime >= 300:
        logTemperature(logFile)
        logTime = time.time()

