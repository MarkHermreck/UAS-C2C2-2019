"""
Property of UAS C2C2 Senior Design Team 2019
Team Members: Mark Hermreck, Joseph Lisac, Khaled Alshammari, Khaled Alharbi
Questions about this code can be directed toward Mark Hermreck at markhermreck@gmail.com
"""

#importing all the functions and sundries needed from dronekit, mavlink, and the navigation module
from dronekit import connect, LocationGlobal, LocationGlobalRelative, Vehicle, VehicleMode
from navigation import takeoffSequence, distanceRelative, searchLocation, travel, searchPattern, landingSequence
from navigation import safetyChecks
import time, math, dronekit_sitl

#importing things needed for communication
import logging
import sys
import wave
from communication import Communication

# Connect to xBee
COM_CONNECTION_STRING = '/dev/ttyUSB0'      #potential option
com = Communication(COM_CONNECTION_STRING, 0.1)

# This block of code connects to the UAV over its serial connection, Pi -> PixHawk
# It also initalizes the vehicle object referenced throughout this file.
# When the connection information is known, fill out the portInformation variable to disable auto-start of SITL.
portInformation = '/dev/ttyAMA0' #'127.0.0.1:14550'
testSITL = None

if not portInformation:
    testSITL = dronekit_sitl.start_default()
    portInformation = testSITL.connection_string()
    print ("Starting SITL Test Environment, No UAV Detected")

#file = open("test.txt", "w+")
#file.write("running")
#file.close()
time.sleep(30)

print("Connecting to UAV.")
UAV = connect(portInformation, wait_ready=True, baud=57600)
print(" Autopilot Firmware version: %s" % UAV.version)
# wait for radio transmission from ground station UI, store transmitted values into this array
# 0-1 are ISU 1 lat/long, 2-3 ISU 2 lat/long, 4-5 gnd station lat/long
# these default coordinates are locations around Palmer Park's drone field, and are default locations the drone can go to if communications fails
# SAFETY NOTE: DON'T MESS UP YOUR COORDINATES. EVEN AN ERROR IN THE TENTH'S PLACE CAN SEND THE DRONE MILES AWAY
GPSCoordinates = [33.175217, -87.605560, 33.175587, -87.605886, 33.175217, -87.605560];


print("receiving waypoints")
waypoints = com.receive()
coordinateFile = open("GPSCoords.txt", "w+")
while waypoints != "EndOfFile":
    if waypoints is not None:
        coordinateFile.write(str(waypoints))
        coordinateFile.write(" ")
    waypoints = com.receive()
coordinateFile.close();

coords = open("GPSCoords.txt", "r")

iteration = 0;
for line in coords:
    for word in line.split():
        GPSCoordinates[iteration] = float(word)
        iteration -= -1

for i in range(len(GPSCoordinates)):
    print(GPSCoordinates[i])

#default location is canberra, australia
#-35.363261
#149.1652299

#print(UAV.location.global_relative_frame.lat)
#print(UAV.location.global_relative_frame.lon)

#declares three LGR objects in case they're needed. Default altitude is also declared here; for now it's 30m
alt = 3;
ISU1Location = LocationGlobalRelative(GPSCoordinates[0], GPSCoordinates[1], alt)
ISU2Location = LocationGlobalRelative(GPSCoordinates[2], GPSCoordinates[3], alt)
GNDLocation = LocationGlobalRelative(GPSCoordinates[4], GPSCoordinates[5], alt)
print("assigns locations")
#takes off and sets the homelocation. alt of it is 0, and is what the LGR's base theirs off of


ISU1Log = open("/home/pi/Documents/ISU1Log.txt", "a+")
ISU1Log.truncate(0)
homeLoc = takeoffSequence(alt, UAV)
travel(GPSCoordinates[0],GPSCoordinates[1], alt, UAV)
UAV.mode = VehicleMode("LOITER")

com.send("Requesting ISU1 data")
ISUOne = com.receive()
noneCounter = 0
searchFlag = 0;
timeout = 5
timeFlag = time.time()
foundFlag = 0
breakFlag = True;
while breakFlag:
    com.send("Requesting ISU1 data")
    ISUOne = com.receive()
    while ISUOne != "EndOfFile":
        noneCounter -= -1
        
        if noneCounter >= 10:
            print(noneCounter)
            print(searchFlag)
            noneCounter = 0
            searchFlag -= -1
            if searchFlag >= 5:
                breakFlag = False
                foundFlag = 0;
                foundFlag = searchPattern(4, UAV.location.global_relative_frame, UAV, 1, com)
            break;
        if ISUOne is not None:
            timeFlag = time.time()
            noneCounter = 0
            ISU1Log.write(ISUOne)
        ISUOne = com.receive()
        if ISUOne == "EndOfFile":
            breakFlag = False;
    
    if not breakFlag:
        ISU1Log.close();
        
    if foundFlag == 1:
        break;

print("exited text")
byteNumber = 0
fileSize = 2 * 204800
audioData = b""
bytesSent = 0
lastBytesSent = 0
f = wave.open("/home/pi/Documents/wav.wav", "w")
#hardcoded file format
n_channels = 1
sample_width = 2
framerate = 44100
n_frames = 204800
comp_type = "NONE"
comp_name = "not compressed"
params = (n_channels, sample_width, framerate, n_frames, comp_type, comp_name)
f.setparams(params)


x = com.receiveAudio()
timeFlag = time.time()
while byteNumber < fileSize:
    #valid data
    if x != b"":
        timeFlag = time.time()
        byteNumber = byteNumber + 1
        #valid data
        #append to data
        audioData = audioData + x
        bytesSent = bytesSent + 1
        if bytesSent >= lastBytesSent + 1024:
           lastBytesSent = lastBytesSent + 1024
           print(lastBytesSent)
                
    x = com.receiveAudio()
    if (timeFlag + timeout < time.time()):
        print("Timeout")
        break
    #transmission finished, write to file
f.writeframesraw(audioData)
f.close()
        

"""
1. ping
2. receive handshaek
3. go stragiht into receive loop
4. receive EOF
5. receive audi ohandshek
6. 
"""
#temp = open("/home/pi/ISU1Log.txt", "w+")
#temp.close()
safetyChecks(UAV,homeLoc)

travel(GPSCoordinates[2],GPSCoordinates[3], alt, UAV)
searchPattern(4, UAV.location.global_relative_frame, UAV, 2, com)
landingSequence(homeLoc,UAV)


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

#ISU1Log = open("ISU1Log.txt", "r")
#ISU2Log = open("ISU2Log.txt", "r")

"""
com.send("ISULog1")
sendTextFile(ISU1Log)
com.send("EndOfFile")
com.send("ISULog2")
sendTextFile(ISU2Log)
com.send("EndOfFile")

"""