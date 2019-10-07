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
from communication import Communication

# Connect to xBee
COM_CONNECTION_STRING = '/dev/ttyUSB1'      #potential option
com = Communication(COM_CONNECTION_STRING, 0.1)

# This block of code connects to the UAV over its serial connection, Pi -> PixHawk
# It also initalizes the vehicle object referenced throughout this file.
# When the connection information is known, fill out the portInformation variable to disable auto-start of SITL.
portInformation = None #'127.0.0.1:14550'
testSITL = None

if not portInformation:
    testSITL = dronekit_sitl.start_default()
    portInformation = testSITL.connection_string()
    print "Starting SITL Test Environment, No UAV Detected"

print("Connecting to UAV.")
UAV = connect(portInformation, wait_ready=True)



# wait for radio transmission from ground station UI, store transmitted values into this array
# 0-1 are ISU 1 lat/long, 2-3 ISU 2 lat/long, 4-5 gnd station lat/long
GPSCoordinates = [-35.364,149.167, -35.365, 149.168, 0, 0];

#default location is canberra, australia
#-35.363261
#149.1652299

print(UAV.location.global_relative_frame.lat)
print(UAV.location.global_relative_frame.lon)

#declares three LGR objects in case they're needed. Default altitude is also declared here; for now it's 30m
alt = 30;
ISU1Location = LocationGlobalRelative(GPSCoordinates[0], GPSCoordinates[1], alt)
ISU2Location = LocationGlobalRelative(GPSCoordinates[2], GPSCoordinates[3], alt)
GNDLocation = LocationGlobalRelative(GPSCoordinates[4], GPSCoordinates[5], alt)


#takes off and sets the homelocation. alt of it is 0, and is what the LGR's base theirs off of
homeLoc = takeoffSequence(alt, UAV)
#travels to first ISU

travel(GPSCoordinates[0],GPSCoordinates[1], alt, UAV)
UAV.mode = VehicleMode("LOITER")
ISUOne = 0; #com.ping()
if not ISUOne:
    safetyChecks(UAV, homeLoc)
    searchPattern(3, UAV.location.global_relative_frame, UAV)
safetyChecks(UAV, homeLoc)


#travels to second ISU location,
travel(GPSCoordinates[2],GPSCoordinates[3], alt, UAV)
UAV.mode = VehicleMode("LOITER")
ISUTwo = 0; #com.ping()
if not ISUTwo:
    safetyChecks(UAV, homeLoc)
    searchPattern(3, UAV.location.global_relative_frame, UAV)
safetyChecks(UAV, homeLoc)

#returns home
landingSequence(homeLoc,UAV)
#com.send()

